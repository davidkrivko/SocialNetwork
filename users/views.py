from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import UserModel
from users.serializers import RegistrationSerializer


class RegistrationApiView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]
