from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.views.chats import ChatsListView, ChatsCreateView

router = DefaultRouter()


urlpatterns = [
    path('list/', ChatsListView.as_view()),
    path('create/', ChatsCreateView.as_view()),
]
urlpatterns += router.urls