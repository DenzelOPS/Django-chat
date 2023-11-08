from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class SessionKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=280)

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.ForeignKey(SessionKey, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField()


