from django.urls import path
from chats.views import (index, chat_detail,
                         chat_list, chat_create, send_message, read_message,
                         chat_messages_list, database_fill)

urlpatterns = [
    path('index', index, name='index'),
    path('detail/<int:pk>', chat_detail, name='chat_detail'),
    path('list', chat_list, name='chat_list'),
    path('create', chat_create, name='chat_create'),
    path('sendmessage', send_message, name='send_message'),
    path('readmessage', read_message, name='message_read'),
    path('messagelist', chat_messages_list, name='messages_list'),
    path('dbfill', database_fill, name='db_fill'),
]
