from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.user import RegistrationSerializer, UserMeSerializer


class UserMeView(RetrieveAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(UpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class RegistrationAPIViews(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



