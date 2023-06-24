from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import Util
from chat.models import ChatRoom
from .models import User

@receiver(post_save, sender=User)
def create_chatroom(sender, instance, created, **kwargs):
    if created:
        user=instance
        user_name=user.name
        user_id=user.id
        room_name=user_name
        #new_chat=ChatRoom.objects.create(name=room_name,user=user)
        #new_chat.save()
        #print('New Chatroom created....')

