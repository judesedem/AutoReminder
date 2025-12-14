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
class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=120)
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields=['username','password']

    
class ReminderSerializer(serializers.ModelSerializer):  
    frequency=serializers.CharField(max_length=1)
    class Meta:
        model=Reminder
        fields='__all__'
        read_only_fields=['user','id']

    def validate_scheduled_time(self,value):
        if value<timezone.now(): #if the user sets a past date
            raise serializers.ValidationError("Set an appropriate date")
            

        return value
    
    def validate_frequency(self,value):
        allowed_values=['O','H','D','W','M']
        if not value: # Giving an appropriate error message
            raise serializers.ValidationError("Field cannot be left empty")
        if value not in allowed_values:
            raise serializers.ValidationError(f"Invalid frequency. Choose from {allowed_values}")
        return value