from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    bio = models.CharField(max_length=10000, null=True)
    nick = models.CharField(max_length=32, null=True)
    avatar = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
