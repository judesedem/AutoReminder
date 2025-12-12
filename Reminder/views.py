from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User=get_user_model()

class RegisterView(CreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[AllowAny]
    queryset=User.objects.all()


from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from . models import Reminder
from . serializers import ReminderSerializer

class ReminderListCreateView(ListCreateAPIView):
    serializer_class=ReminderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)           

        
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


from rest_framework.generics import RetrieveUpdateDestroyAPIView 
from rest_framework.response import Response
from rest_framework import status     
class ReminderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class=ReminderSerializer
    permission_classes=[IsAuthenticated]
    

    def get_queryset(self):        
        return Reminder.objects.filter(user=self.request.user)


    def destroy(self,request,*args,**kwargs):
        instance=self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message":"Reminder deleted successfully!"},
            status=status.HTTP_200_OK
        )