from django.contrib import admin

from forum.models import (
    Section,
    Theme,
    Message,
)


@admin.register(Section)
class BikeModificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
    )


@admin.register(Theme)
class BikeModificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "section",
        "messages_count",
        "created_at",
    )


@admin.register(Message)
class BikeModificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content",
        "parent_id",
        "author",
        "theme",
        "created_at",
    )