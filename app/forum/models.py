from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Theme(models.Model):
    section = models.ForeignKey(
        "Section",
        on_delete=models.PROTECT,
        related_name="theme",
    )
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="theme",
    )
    messages_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("theme", kwargs={"theme_id": self.pk})


class Message(models.Model):
    theme = models.ForeignKey(
        "Theme",
        on_delete=models.CASCADE,
        related_name="message",
    )
    content = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="theme",
    )
    parent_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("message", kwargs={"message_id": self.pk})