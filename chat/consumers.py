"""
WebSocket consumer для обработки сообщений.

Атрибуты:
    master_key (bytes): Главный ключ шифрования, используемый для шифрования и дешифрования сообщений.

Методы:
    get_chat_history: Получите историю чата.
    connect: Обработка соединения WebSocket
    disconnect: Обработка закрытия WebSocket.
    receive: Обработка входящих сообщений.
    send_message: Отправка сообщений.
"""

import json
import os
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, SessionKey, ChatRoom
from chat.services import encrypt, decrypt


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master_key = bytes(os.getenv('ENCRYPTION_KEY'), 'utf-8')
    
    async def get_chat_history(self):
        chat_room_id = self.scope["url_route"]["kwargs"]["chat_room_id"]
        chat_history_data = await self.get_chat_history_async(chat_room_id, self.master_key)
        
        await self.send(text_data=json.dumps({'chat_history': chat_history_data}))


    @staticmethod
    @sync_to_async
    def get_chat_history_async(chat_room_id, master_key):
        chat_history = Message.objects.filter(chat_room_id=chat_room_id)
        chat_history_data = []

        for message in chat_history:
            chat_history_data.append({
                'message': decrypt(message.text, decrypt(message.key.key.encode(), master_key).encode()),
                'username': message.sender.username,
            })

        return chat_history_data
    
    
    async def connect(self):
        self.chat_room_id = self.scope["url_route"]["kwargs"]["chat_room_id"]
        self.room_group_name = f"chat_{self.chat_room_id}"
        self.key = await sync_to_async(SessionKey.objects.get)(id = self.scope["session"]['session_key_id'])      
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.get_chat_history()
        
        
    async def disconnect(self , close_code):
        del self.scope["session"]['session_key']
        
        await self.channel_layer.group_discard(
            self.room_group_name , 
            self.channel_name 
        )
        
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        chat_room = await database_sync_to_async(get_object_or_404)(ChatRoom, id=self.chat_room_id)
        
        await database_sync_to_async(Message.objects.create)(
            chat_room=chat_room,
            sender=self.scope["user"],
            key=self.key,
            text=encrypt(text_data_json["message"], self.scope["session"]["session_key"].encode()).decode(),
            timestamp=timezone.now()
        )

        await self.channel_layer.group_send(
            self.room_group_name,{
                "type" : "send_message" ,
                "message" : text_data_json["message"] , 
                "username" : text_data_json["username"] ,
            })
        
        
    async def send_message(self , event) : 
        message = event["message"]
        username = event["username"]
        
        await self.send(text_data = json.dumps({"message":message ,"username":username}))