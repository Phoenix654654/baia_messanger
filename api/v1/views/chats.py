from django.db import transaction
from rest_framework import status, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers.chats import ChatMemberCreateSerializer, \
    ChatSerializer, ChatAddMemberSerializer, ChatListSerializer, ChatRemoveMemberSerializer, ChatDetailSerializer, \
    MessageSerializer, MessageListSerializer, MessageUpdateSerializer
from apps.abstract.custom_class import CustomPagination
from apps.chats.models import Chat, ChatMember, Messages
from apps.user.models import User


class ChatListView(ListAPIView):
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Chat.objects.filter(chat__user=self.request.user).distinct()


class ChatPersonalCreateView(CreateAPIView):
    serializer_class = ChatMemberCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        other_user_id = request.data.get('user')
        if not other_user_id:
            return Response({"error": "Other user ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Check if a personal chat already exists between the users
        existing_chat = Chat.objects.filter(
            is_group=False,
            chat__is_deleted=False,
            chat__user=request.user
        ).filter(
            chat__user=other_user
        ).first()

        if existing_chat:
            return Response({"chat_id": existing_chat.id}, status=status.HTTP_200_OK)

        # Create the chat and chat members within a transaction
        with transaction.atomic():
            chat = Chat.objects.create(is_group=False)
            ChatMember.objects.create(user=request.user, chat=chat)
            ChatMember.objects.create(user=other_user, chat=chat)

        return Response({"chat_id": chat.id}, status=status.HTTP_201_CREATED)


class ChatGroupCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        chat = serializer.save(is_group=True)
        ChatMember.objects.create(
            user=self.request.user,
            chat=chat,
            is_admin=True
        )
        return chat

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Групповой чат успешно создан", "data": response.data}, status=status.HTTP_201_CREATED)


class ChatGroupUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    queryset = Chat.objects.filter(is_group=True)
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        # Customize update logic if needed
        chat = serializer.save()
        return chat


class ChatAddMemberView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatAddMemberSerializer

    def perform_create(self, serializer):
        chat = serializer.validated_data['chat']
        user_ids = serializer.validated_data['user_ids']

        users = User.objects.filter(id__in=user_ids)
        if not users.exists():
            raise serializers.ValidationError({"error": "Пользователи не найдены."})

        for user in users:
            ChatMember.objects.get_or_create(chat=chat, user=user)


class ChatRemoveMemberView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRemoveMemberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        chat_id = serializer.validated_data['chat_id']
        user_ids = serializer.validated_data['user_ids']
        ChatMember.objects.filter(chat_id=chat_id, user_id__in=user_ids).delete()

        return Response({"message": "Пользователи успешно удалены из группы."}, status=status.HTTP_200_OK)



class ChatDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)

        # Сериализация данных чата и его участников
        serializer = ChatDetailSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Добавляем текущего аутентифицированного пользователя как отправителя сообщения
        serializer.save(user=self.request.user)  # Привязываем сообщение к текущему пользователю

    def create(self, request, *args, **kwargs):
        # Модифицируем ответ, если нужно
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Сообщение успешно отправлено", "data": response.data}, status=status.HTTP_201_CREATED)


class MessageDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Messages.objects.all()
    lookup_field = 'id'  # Будем искать сообщение по полю 'id'

    def perform_destroy(self, instance):
        # Проверка: сообщение принадлежит текущему пользователю
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить это сообщение.")
        # Или: проверка, что пользователь является членом чата (если нужно)
        # if not instance.chat.members.filter(user=self.request.user).exists():
        #     raise PermissionDenied("Вы не можете удалить это сообщение.")

        super().perform_destroy(instance)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({"message": "Сообщение успешно удалено"}, status=status.HTTP_204_NO_CONTENT)


class MessageListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')  # Получаем chat_id из URL
        return Messages.objects.filter(chat_id=chat_id).order_by('created_at')


class MessageUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageUpdateSerializer
    queryset = Messages.objects.all()  # Or you can set the queryset in the get_queryset method

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return Messages.objects.filter(chat_id=chat_id)

    def update(self, request, *args, **kwargs):
        # The pk is automatically passed in the kwargs due to URL pattern change
        instance = self.get_object()

        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to edit this message.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

