from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from django.views.static import serve
from django.conf import settings


class MediaViewSet(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return serve(request, kwargs.get("path"), document_root=settings.MEDIA_ROOT, show_indexes=False)
