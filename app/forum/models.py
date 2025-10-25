from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"])
        ]


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
        return reverse(
            "messages_on_theme",
            kwargs={
                "section_id": self.section.pk,
                "theme_id": self.pk,
            },
        )

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"])
        ]


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
        related_name="message",
    )
    parent = models.ForeignKey(
        "Message",
        on_delete=models.PROTECT,
        related_name="all_parents",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"])
        ]