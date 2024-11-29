from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.chats import ChatsListSerializer, ChatsCreateSerializer
from apps.chats.models import Chat


class ChatsListView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatsListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter()


class ChatsCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatsCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        response_serializer = ChatsListSerializer(chat)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ChatsDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatsCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter()


