from django.contrib import admin

from forum.models import (
    Section,
    Theme,
    Message,
)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
    )


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "section",
        "messages_count",
        "created_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content",
        "parent_id",
        "author",
        "theme",
        "created_at",
        "is_active",
    )