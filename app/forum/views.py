from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
)

from forum.forms import (
    CreateThemeForm,
    CreateMessageForm,
)
from forum.models import (
    Theme,
    Message,
)
from forum.utils import DataMixin


class ShowAbout(DataMixin, TemplateView):
    template_name = "forum/about.html"
    title_page = "О себе"


class HomePage(DataMixin, ListView):
    model = Theme
    template_name = "forum/index.html"
    title_page = "Главная"
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
    form_class = CreateMessageForm
    template_name = "forum/create_message.html"
    title_page = "Новое сообщение"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        theme_id = self.kwargs["theme_id"]
        theme = Theme.objects.get(pk=theme_id)

        return self.get_mixin_context(
            context,
            theme=theme,
        )

    def form_valid(self, form):
        context = self.get_context_data()
        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        theme = context["theme"]

        form.instance.author = self.request.user
        form.instance.theme = theme

        self.object = form.save()
        self.success_url = reverse_lazy(
            "messages_on_theme",
            kwargs={
                "section_id": section_id,
                "theme_id": theme_id,
            },
        )
        return super().form_valid(form)


class CreateTheme(LoginRequiredMixin, DataMixin, CreateView):
    model = Theme
    form_class = CreateThemeForm
    template_name = "forum/create_theme.html"
    title_page = "Новая тема"

    def form_valid(self, form):
        form.instance.author = self.request.user

        self.object = form.save()

        section_id = self.object.section.pk
        theme_id = self.object.pk

        self.success_url = reverse_lazy(
            "messages_on_theme",
            kwargs={
                "section_id": section_id,
                "theme_id": theme_id,
            },
        )
        return super().form_valid(form)