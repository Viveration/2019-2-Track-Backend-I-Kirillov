from django.db import models
# from userprofile.models import User


class Chat(models.Model):
    topic = models.CharField(max_length=32, null=False)
    last_message = models.CharField(max_length=65536, null=True)
    is_group_chat = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'chat'
        verbose_name_plural = 'chats'


class Message(models.Model):
    chat = models.ForeignKey('chats.Chat', on_delete=models.PROTECT)
    user = models.ForeignKey('userprofile.User', on_delete=models.PROTECT)
    content = models.CharField(max_length=65536, null=True)
    # added_at = models.DateField()

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'


class Attachment(models.Model):
    chat = models.ForeignKey('chats.Chat', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey('userprofile.User', on_delete=models.PROTECT)
    message = models.ForeignKey('chats.Message', on_delete=models.PROTECT)
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'attach'
        verbose_name_plural = 'attaches'


class Member(models.Model):
    user = models.ForeignKey('userprofile.User', on_delete=models.PROTECT, null=True)
    chat = models.ManyToManyField('chats.Chat', null=True)
    new_messages = models.CharField(max_length=32, null=True)
    last_read_message = models.ForeignKey('chats.Message', null=True,  on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
