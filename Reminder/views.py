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
from .tasks import schedule_reminder_task
class ReminderListCreateView(ListCreateAPIView):
    serializer_class=ReminderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)  
             

        
    
    def perform_create(self,serializer):
       reminder=serializer.save(user=self.request.user)
       schedule_reminder_task(reminder)



from rest_framework.generics import RetrieveUpdateDestroyAPIView 
from rest_framework.response import Response
from rest_framework import status   
from .tasks import schedule_reminder_task  
from django_q.models import Schedule
class ReminderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class=ReminderSerializer
    permission_classes=[IsAuthenticated]
    

    def get_queryset(self):        
        return Reminder.objects.filter(user=self.request.user)

    def update(self,request,*args,**kwargs):
        response=super().update(request,*args,**kwargs)

        reminder=self.get_object()

        schedule_reminder_task(reminder)

        return response
    
    def destroy(self,request,*args,**kwargs):
        instance=self.get_object()

        try:
            Schedule.objects.filter(name=f"reminder_{instance.id}").delete()
            print(f"Cancelled scheduled task for reminder {instance.id}")
        except Exception as e:
            print(f"Could not cancel task: {e}")

        self.perform_destroy(instance)

        
        return Response(
            {"message":"Reminder deleted successfully!"},
            status=status.HTTP_200_OK
        )
    
