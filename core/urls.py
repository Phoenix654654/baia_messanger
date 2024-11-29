from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth import views as auth_views, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API for user registration",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

def logout_view(request):
    logout(request)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('api.v1.urls.user')),
    path('api/chats/', include('api.v1.urls.chats')),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
