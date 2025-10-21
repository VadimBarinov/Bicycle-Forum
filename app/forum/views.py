from django.views.generic import TemplateView

from forum.utils import DataMixin


class HomePage(DataMixin, TemplateView):
    template_name = 'forum/index.html'
    title_page = 'Главная'
