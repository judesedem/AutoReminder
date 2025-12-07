from rest_framework import serializer
from .models import  Reminder,User



class ReminderSerializer(serializer.ModelSerializer):
    class Meta:
        model=Reminder
        fields='__all__'

class SignupSerializer(serializer.ModelSerializer):
    username=serializer.CharField(min_length=10)
    password=serializer.CharField(min_length=8, write_only=True)

    class Meta:
        model=User
        fields=('username','password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username']            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_user(self,value):
        if User.objects.filter(username=value).exists():
            raise serializer.ValidationError("Username already exists")
    
class LoginSerializer(serializer.ModelSerializer):
    username=serializer.CharField()
    password=serializer.CharField(write_only=True)

    def validate_user(self,attrs):
        username=attrs.get(username)
        password=attrs.get(password)

        user=User.objects.filter(username=username).first()
        if not user:
            raise serializer.ValidationError("Invalid username or password")
        
        if not user.checkpassword(password):
            if not user:
                raise serializer.ValidationError("Invalid username or password")
            
        attrs['user'] = user
        return attrs
    
