from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.views.chats import ChatPersonalCreateView, ChatGroupCreateView, ChatAddMemberView, \
    ChatGroupUpdateView, ChatListView, ChatRemoveMemberView, ChatDetailView, MessageCreateView, MessageDeleteView, \
    MessageListView, MessageUpdateView

router = DefaultRouter()
# router.register(r'chat/<int:chat_id>/messages', MessageListView, basename='message-list')


urlpatterns = [
    path('personal/create/', ChatPersonalCreateView.as_view()),
    path('group/create/', ChatGroupCreateView.as_view(), name='create_chat'),
    path('chats/<int:chat_id>/add-members/', ChatAddMemberView.as_view(), name='add_chat_members'),
    path('chats/<int:pk>/update/', ChatGroupUpdateView.as_view(), name='chat-group-update'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/remove-members/', ChatRemoveMemberView.as_view(), name='chat-remove-members'),
    path('chats/<int:chat_id>/', ChatDetailView.as_view(), name='chat-detail'),

    path('messages/', MessageCreateView.as_view(), name='message-create'),
    path('message/<int:id>/', MessageDeleteView.as_view(), name='message-delete'),
    path('messages/<int:chat_id>/', MessageListView.as_view(), name='message-list'),
    path('<int:chat_id>/messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message-update'),
]
urlpatterns += router.urls