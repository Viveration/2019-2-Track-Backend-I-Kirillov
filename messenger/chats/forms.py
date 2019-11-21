from django import forms
from models.py import Chat, Message


class MessageSendForm(forms.Form):
    class Meta:
        model = Message
        fields = ['content', 'added_at']


class ChatCreateForm(forms.Form):
    class Meta:
        model = Chat
        fields = ['topic']
