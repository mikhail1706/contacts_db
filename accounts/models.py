from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatar.svg')

    class Meta:
        db_table = 'custom_user'
