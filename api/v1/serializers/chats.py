from rest_framework import serializers

from apps.chats.models import Chat, ChatMember


class ChatMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = (
            "user",
        )


class ChatsCreateSerializer(serializers.ModelSerializer):
    chat_members = ChatMemberCreateSerializer(many=True, read_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Chat
        fields = (
            "is_group",
            "name",
            "avatar",
            "chat_members",
        )
        extra_kwargs = {"name": {"required": False}, "avatar": {"required": False}}

    def create(self, validated_data):
        chat_members_data = validated_data.pop("chat_members", [])
        chat = Chat.objects.create(**validated_data)
        current_user = self.context['request'].user

        ChatMember.objects.get_or_create(
            chat=chat,
            user=current_user,
            defaults={"is_admin": True}
        )

        for member_data in chat_members_data:
            user = member_data.get("user")
            if not user:
                continue

            chat_member = ChatMember.objects.filter(chat=chat, user=user).first()

            if chat_member:
                if chat_member.is_deleted:
                    chat_member.is_deleted = False
                    chat_member.save(update_fields=["is_deleted"])
            else:
                ChatMember.objects.create(chat=chat, **member_data)

        return chat
class ChatsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "id",
            "is_group",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
        )
