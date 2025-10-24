from django.views.generic import TemplateView, ListView

from forum.models import Theme
from forum.utils import DataMixin


class ShowAbout(DataMixin, TemplateView):
    template_name = 'forum/about.html'
    title_page = 'О себе'


class HomePage(DataMixin, ListView):
    model = Theme
    template_name = 'forum/index.html'
    title_page = 'Главная'
    context_object_name = "themes"
