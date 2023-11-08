from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from chat import views as chat_views
from .forms import Log_in_form

urlpatterns = [
    path('', chat_views.main_page, name='chat-page'),
    path('create-chat-room/', chat_views.create_chat_room, name='create-chat-room'),
    path('chat-rooms/', chat_views.chat_rooms, name='chat-rooms'),
    path('chat-room/<int:chat_room_id>/', chat_views.chat_room, name='chat-room'),
    path('auth/login/', chat_views.login_user, name='login-user'),
    path('auth/register/', chat_views.register, name='register-user'),  # Add this line
    path('auth/logout/', LogoutView.as_view(), name='logout-user'),
]
