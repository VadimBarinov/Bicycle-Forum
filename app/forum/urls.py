from django.urls import path

from .views import (
    HomePage,
    ShowAbout,
    MessagesOnThemeList,
    CreateMessage,
    CreateTheme,
)

urlpatterns = [
    path(
        "",
        HomePage.as_view(),
        name="home",
    ),
    path(
        "about/",
        ShowAbout.as_view(),
        name="about",
    ),
    path(
        "section/<int:section_id>/theme/<int:theme_id>/",
        MessagesOnThemeList.as_view(),
        name="messages_on_theme",
    ),
    path(
        "section/<int:section_id>/theme/<int:theme_id>/create_message/",
        CreateMessage.as_view(),
        name="create_message",
    ),
    path(
        "create_theme/",
        CreateTheme.as_view(),
        name="create_theme",
    ),
]
