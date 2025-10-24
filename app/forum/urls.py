from django.urls import path

from .views import (
    HomePage,
    ShowAbout,
    ThemeDetail,
    CreateMessage,
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
        ThemeDetail.as_view(),
        name="theme",
    ),
    path(
        "section/<int:section_id>/theme/<int:theme_id>/create_message/",
        CreateMessage.as_view(),
        name="create_message",
    ),
    path(
        "section/<int:section_id>/create_theme/",
        CreateMessage.as_view(),
        name="create_message",
    ),
]
