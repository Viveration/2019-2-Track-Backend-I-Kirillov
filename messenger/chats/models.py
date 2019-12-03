from django.db import models
# from userprofile.models import User


class Chat(models.Model):
    topic = models.CharField(max_length=32, null=False)
    last_message = models.CharField(max_length=65536, null=True)
    is_group_chat = models.BooleanField(default=True)
    chat_avatar = models.FileField(upload_to='images/', null=True)

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'


class Message(models.Model):
    chat = models.ForeignKey('chats.Chat', on_delete=models.CASCADE)
    user = models.ForeignKey('userprofile.User', on_delete=models.CASCADE)
    content = models.CharField(max_length=65536, null=True)
    added_at = models.DateTimeField(null=True, auto_now_add=True)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Attachment(models.Model):
    chat = models.ForeignKey('chats.Chat', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('userprofile.User', on_delete=models.CASCADE)
    message = models.ForeignKey('chats.Message', on_delete=models.CASCADE)
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'вложение'
        verbose_name_plural = 'вложения'


class Member(models.Model):
    user = models.ForeignKey('userprofile.User', on_delete=models.CASCADE, null=False)
    chat = models.ForeignKey('chats.Chat', null=False,  on_delete=models.CASCADE)
    new_messages = models.CharField(max_length=32, null=True)
    last_read_message = models.ForeignKey('chats.Message', null=True,  on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
