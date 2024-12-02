from PIL import Image
from rest_framework import serializers

from apps.chats.models import Chat, ChatMember, Messages
from apps.user.models import User


class ChatMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = (
            "user",
        )


class ChatListSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'name', 'avatar', 'is_group', 'members']

    def get_members(self, obj):
        members = ChatMember.objects.filter(chat=obj).select_related('user')
        return [{"id": member.user.id, "name": member.user.username} for member in members]


class ChatSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Chat
        fields = ['name', 'avatar']

    # def validate_avatar(self, value):
    #     if value.size > 2 * 1024 * 1024:  # Ограничение: 2 МБ
    #         raise serializers.ValidationError("Размер изображения не должен превышать 2 МБ")
    #
    #     try:
    #         img = Image.open(value)
    #         if img.format not in ['JPEG', 'PNG']:
    #             raise serializers.ValidationError("Поддерживаются только форматы JPEG и PNG")
    #     except Exception:
    #         raise serializers.ValidationError("Ошибка обработки изображения")
    #     return value


class ChatAddMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="Список ID пользователей для добавления"
    )

    def validate(self, attrs):
        request = self.context['request']
        chat_id = self.context['view'].kwargs.get('chat_id')
        chat = Chat.objects.filter(id=chat_id, is_group=True).first()

        if not chat:
            raise serializers.ValidationError("Чат не найден или не является групповым.")

        # Проверяем, что текущий пользователь является администратором
        is_admin = ChatMember.objects.filter(chat=chat, user=request.user, is_admin=True).exists()
        if not is_admin:
            raise serializers.ValidationError("У вас нет прав добавлять участников в этот чат.")

        attrs['chat'] = chat
        return attrs


class ChatRemoveMemberSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField()
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        write_only=True
    )

    def validate(self, attrs):
        chat_id = attrs.get('chat_id')
        user_ids = attrs.get('user_ids')

        try:
            chat = Chat.objects.get(id=chat_id, is_group=True)
        except Chat.DoesNotExist:
            raise serializers.ValidationError({"chat_id": "Групповой чат не найден."})

        if not ChatMember.objects.filter(chat=chat, user=self.context['request'].user, is_admin=True).exists():
            raise serializers.ValidationError("Вы не являетесь администратором группы.")

        invalid_users = User.objects.filter(id__in=user_ids).exclude(chat_member__chat=chat)
        if invalid_users.exists():
            raise serializers.ValidationError(
                {"user_ids": f"Пользователи с ID {', '.join(map(str, invalid_users.values_list('id', flat=True)))} не являются участниками группы."}
            )

        return attrs


class ChatMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Или можно использовать более детализированное отображение пользователя

    class Meta:
        model = ChatMember
        fields = ['user', 'is_admin', 'is_deleted', 'joined_at', 'leave_at']


# Сериализатор для чата
class ChatDetailSerializer(serializers.ModelSerializer):
    members = ChatMemberSerializer(source='chat', many=True)

    class Meta:
        model = Chat
        fields = ['id', 'is_group', 'name', 'avatar', 'created_at', 'updated_at', 'deleted_at', 'members']


class MessageSerializer(serializers.ModelSerializer):
    file_url = serializers.ImageField(required=False)

    class Meta:
        model = Messages
        fields = ['chat', 'text', 'file_url']  # Поля, которые можно отправлять в запросе

    def validate_chat(self, value):
        # Дополнительная логика для валидации чата (например, проверка существования чата)
        if not value:
            raise serializers.ValidationError("Chat is required.")
        return value

    def validate_user(self, value):
        # Проверка, чтобы пользователь был участником чата
        if not value.chat_member.filter(chat=value).exists():
            raise serializers.ValidationError("User is not a member of this chat.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageListSerializer(serializers.ModelSerializer):
    file_url = serializers.ImageField(required=False)
    user = UserSerializer()

    class Meta:
        model = Messages
        fields = ['chat', 'user', 'text', 'file_url']


class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['text', 'file_url']

