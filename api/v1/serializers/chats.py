from rest_framework import serializers

from apps.chats.models import Chat


class ChatsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "is_group",
            "name",
        )
        extra_kwargs = {"name": {"required": False}}


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