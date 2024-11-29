from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.views.views import RegistrationAPIViews, UserMeView, UserUpdateView

router = DefaultRouter()


urlpatterns = [
    path('me/', UserMeView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('regisration/', RegistrationAPIViews.as_view()),
]
urlpatterns += router.urls