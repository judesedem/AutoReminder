from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Reminder

User=get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta(object):
        model=User
        fields=['username','email','password']
    
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ReminderSerializer(serializers.ModelSerializer):    
    class Meta:
        model=Reminder
        fields='__all__'
        read_only_fields=['user','id']

    def validate_scheduled_time(self,value):
        if value<timezone.now():
            raise serializers.ValidationError("Set an appropriate date")

        return value