from django.views.generic import TemplateView, ListView

from forum.utils import DataMixin


class ShowAbout(DataMixin, TemplateView):
    template_name = 'forum/about.html'
    title_page = 'О себе'


class HomePage(DataMixin, TemplateView):
    template_name = 'forum/index.html'
    title_page = 'Главная'
