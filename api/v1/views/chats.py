from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.chats import ChatsListSerializer, ChatsCreateSerializer
from apps.chats.models import Chat


# class ChatViewSet(ModelViewSet):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
#
#     @action(detail=False, methods=['post'])
#     def create_personal_chat(self, request):
#         user_ids = request.data.get('user_ids')
#         if len(user_ids) != 2:
#             return Response({'error': 'Для персонального чата необходимо два пользователя.'}, status=400)
#
#         # Проверьте, есть ли уже чат между этими пользователями
#         chats = Chat.objects.filter(is_group=False)
#         for chat in chats:
#             member_ids = chat.chatmember_set.values_list('user_id', flat=True)
#             if set(user_ids) == set(member_ids):
#                 return Response({'message': 'Персональный чат уже существует.', 'chat_id': chat.id})
#
#         # Создаем новый чат
#         chat = Chat.objects.create(is_group=False)
#         for user_id in user_ids:
#             ChatMember.objects.create(chat=chat, user_id=user_id)
#         return Response({'message': 'Персональный чат создан.', 'chat_id': chat.id})
#
#     @action(detail=False, methods=['post'])
#     def create_group_chat(self, request):
#         group_name = request.data.get('name')
#         user_ids = request.data.get('user_ids')
#         if not group_name or not user_ids:
#             return Response({'error': 'Необходимо указать имя группы и пользователей.'}, status=400)
#
#         # Создаем новый групповой чат
#         chat = Chat.objects.create(is_group=True, name=group_name)
#         for user_id in user_ids:
#             ChatMember.objects.create(chat=chat, user_id=user_id, is_admin=False)
#         return Response({'message': 'Групповой чат создан.', 'chat_id': chat.id})


class ChatsListView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatsListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter()


class ChatCreateView(CreateAPIView):
    serializer_class = ChatsCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ChatsDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatsCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter()


