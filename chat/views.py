"""
Представления Django для функций, связанных с чатом.

Функции:
    set_session_key(request): Установливает ключ сессии.
    register(request): Обработка регистрации пользователей.
    login_user(request): Обработка авторизации пользователя.
    create_chat_room(request): Создание нового чата.
    main_page(request, *args, **kwargs): Главная страница.
    chat_room(request, chat_room_id): Показ определенного чата.
    chat_rooms(request): Показ всех чатов.
"""

import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegistrationForm, ChatRoomForm, Log_in_form
from .models import ChatRoom, SessionKey
from chat.services import generate_session_key, encrypt


def set_session_key(request):
    if 'session_key' not in request.session:
        session_key = generate_session_key().decode()
        request.session["session_key"] = session_key
        master_key = bytes(os.getenv('ENCRYPTION_KEY'), 'utf-8')
        key = SessionKey.objects.create(user=request.user, key=encrypt(session_key, master_key).decode())     
        request.session["session_key_id"] = key.id


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            set_session_key(request)
            return redirect('chat-page')
    else:
        form = RegistrationForm()
    return render(request, 'chat/registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = Log_in_form(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            set_session_key(request)
            return redirect('chat-page')
    else:
        form = Log_in_form()
    return render(request, 'chat/login_page.html', {'form': form})


@login_required()
def create_chat_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.creator = request.user
            chat_room.save()
            return redirect('chat-page')
    else:
        form = ChatRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form}) 


@login_required()
def main_page(request, *args, **kwargs):
    return render(request, "chat/chat_page.html")


@login_required()
def chat_room(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    return render(request, "chat/chat_room.html", {'chat_room': chat_room})


@login_required()
def chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/chat_rooms.html', {'chat_rooms': chat_rooms})