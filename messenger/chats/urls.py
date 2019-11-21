from django.urls import path
from chats.views import index, chat_detail, chat_list, chat_create, send_message, message_read

urlpatterns = [
    path('index/', index, name='index'),
    path('detail/<int:pk>/', chat_detail, name='chat_detail'),
    path('list/<int:uid>/', chat_list, name='chat_list'),
    path('createchat/<int:uid>', chat_create, name='chat_create'),
    path('sendmessage/<int:uid>', send_message, name='send_message'),
    path('readmessage/<int:uid>', message_read, name='message_read'),
]
