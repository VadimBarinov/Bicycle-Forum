from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/",
        blank=True,
        null=True,
        )
