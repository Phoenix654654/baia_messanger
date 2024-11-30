from django.db import models

from apps.user.models import User


class Chat(models.Model):
    is_group = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to='groups/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'chat'
        ordering = ('id',)


class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_member')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    leave_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'chat_member'
        ordering = ('id',)


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message_chat')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user')
    text = models.TextField()
    file_url = models.ImageField(upload_to='messages/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'messages'
        ordering = ('id',)


class MessagesStatus(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='status_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_messages_user')
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'messages_status'
        ordering = ('id',)