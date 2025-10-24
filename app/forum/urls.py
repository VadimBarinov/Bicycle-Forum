from django.urls import path

from .views import (
    HomePage,
    ShowAbout,
)

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("about/", ShowAbout.as_view(), name="about"),
]