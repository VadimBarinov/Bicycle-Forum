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
    list_display_links = (
        "id",
        "title",
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
    list_display_links = (
        "id",
        "title",
    )
    fields = [
        "title",
        "section",
    ]
    def save_model(self, request, obj, form, change):
        if getattr(obj, "author", None) is None:
            obj.author = request.user
        obj.save()

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content",
        "parent",
        "author",
        "theme",
        "created_at",
        "is_active",
    )
    list_display_links = (
        "id",
        "content",
    )
    fields = [
        "theme",
        "content",
        "parent",
        "is_active",
    ]
    def save_model(self, request, obj, form, change):
        if getattr(obj, "author", None) is None:
            obj.author = request.user
        obj.save()