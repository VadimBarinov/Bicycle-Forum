from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from forum.models import Theme, Message, Section
from forum.utils import DataMixin


class ShowAbout(DataMixin, TemplateView):
    template_name = "forum/about.html"
    title_page = 'О себе'


class HomePage(DataMixin, ListView):
    model = Theme
    template_name = "forum/index.html"
    title_page = 'Главная'
    context_object_name = "themes"
    paginate_by = 10


class MessagesOnThemeList(DataMixin, ListView):
    model = Message
    template_name = "forum/messages_on_theme.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        # нужно будет учитывать строку поиска
        return Message.objects.filter(
            theme__pk=self.kwargs["theme_id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        title = Theme.objects.get(pk=theme_id).title

        return self.get_mixin_context(
            context,
            theme_id=theme_id,
            section_id=section_id,
            title=title,
        )


class CreateMessage(LoginRequiredMixin, DataMixin, CreateView):
    model = Message
    fields = '__all__'
    template_name = "forum/create_message.html"
    success_url = reverse_lazy("theme")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     title = self.kwargs["theme_id"]
    #
    #     return self.get_mixin_context(
    #         context,
    #         title=title,
    #     )


class CreateTheme(LoginRequiredMixin, DataMixin, CreateView):
    model = Theme
    fields = '__all__'
    template_name = "forum/create_theme.html"
    success_url = reverse_lazy("home")