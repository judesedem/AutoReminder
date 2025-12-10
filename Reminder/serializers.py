from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reminder

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['username','email','password']

class ReminderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Reminder
        fields=['title','note','reminditem.username']