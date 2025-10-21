from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("forum.urls")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Форум'

handler404 = page_not_found