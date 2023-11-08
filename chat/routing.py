from django.urls import path , include, re_path
from chat.consumers import ChatConsumer
 
# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path(r'chat-room/(?P<chat_room_id>\d+)/', ChatConsumer.as_asgi()),
]
