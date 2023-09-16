from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserModel
from users.serializers import RegistrationSerializer, LastActivityUserSerializer


class RegistrationApiView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]


class UserOnlineStatusApiView(APIView):
    def get(self, request, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
        except:
            return Response(
                {"errors": "User doesn't exist!"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LastActivityUserSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
