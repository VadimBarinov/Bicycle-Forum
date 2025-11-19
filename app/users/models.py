from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/",
        blank=True,
        null=True,
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
