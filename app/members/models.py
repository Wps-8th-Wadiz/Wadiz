from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(
        upload_to='user',
        default='user/blank_user.png'
    )

    nickname = models.CharField(max_length=16)

    def __str__(self):
        return self.username
