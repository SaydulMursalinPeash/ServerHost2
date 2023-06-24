from rest_framework import serializers
from rest_framework import response
from .models import *
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','is_admin','is_officer']
class ChatRoomSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=ChatRoom
        fields=['name','user']

class MessageSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    chat_room=ChatRoomSerializer()
    class Meta:
        model=Message
        fields=['message','user','chat_room','time']