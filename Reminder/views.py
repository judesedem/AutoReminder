from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User=get_user_model()

class RegisterView(CreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[AllowAny]
    queryset=User.objects.all()
