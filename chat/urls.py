from django.urls import path
from .views import *

urlpatterns = [
    path('messages/<room_name>/',RoomMessage.as_view(),name='get_all_message'),
    path('chat-rooms/',AllChatRooms.as_view(),name='get_all_chat_rooms'),
    path('chat-method-rooms/',ChatMethodRooms.as_view(),name='chat_method_rooms'),
    path('all-officers/',AllOfficers.as_view(),name='get-all-officers'),
    path('add-officer-role/',AddOfficerRole.as_view(),name='add-officer-roll'),

]
