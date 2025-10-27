from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import (
    Q,
    F,
    Value,
    CharField,
)
from django.db.models.functions import Concat
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

    def get_queryset(self):
        all_themes = Theme.objects.all()
        query = self.request.GET.get("query")
        if query:
            object_list = all_themes.annotate(
                section_and_title_and_author=Concat(
                    F("section__title"),
                    Value(" "),
                    F("title"),
                    Value(" "),
                    F("author__username"),
                    output_field=CharField(),
                )
            ).filter(
                Q(section_and_title_and_author__icontains=query)
            )
            return object_list
        return all_themes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        input_value = self.request.GET.get("query")
        return self.get_mixin_context(
            context,
            input_value=input_value,
        )

class MessagesOnThemeList(DataMixin, ListView):
    model = Message
    template_name = "forum/messages_on_theme.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        all_messages = Message.objects.filter(
            theme__pk=self.kwargs["theme_id"]
        )
        query = self.request.GET.get("query")
        if query:
            object_list = all_messages.annotate(
                content_and_author=Concat(
                    F("content"),
                    Value(" "),
                    F("author__username"),
                    output_field=CharField(),
                )
            ).filter(
                Q(content_and_author__icontains=query)
            )
            return object_list
        return all_messages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        input_value = self.request.GET.get("query")
        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        title = Theme.objects.get(pk=theme_id).title

        return self.get_mixin_context(
            context,
            input_value=input_value,
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
        theme = context["theme"]
        form.instance.author = self.request.user
        form.instance.theme = theme
        return super().form_valid(form)

    def get_success_url(self):
        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        return reverse_lazy(
            "messages_on_theme",
            kwargs={
                "section_id": section_id,
                "theme_id": theme_id,
            },
        )


class CreateTheme(LoginRequiredMixin, DataMixin, CreateView):
    model = Theme
    form_class = CreateThemeForm
    template_name = "forum/create_theme.html"
    title_page = "Новая тема"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        section_id = self.object.section.pk
        theme_id = self.object.pk
        return reverse_lazy(
            "messages_on_theme",
            kwargs={
                "section_id": section_id,
                "theme_id": theme_id,
            },
        )
