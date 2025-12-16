from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    redirect,
    get_object_or_404
)
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
)

from forum.forms import (
    CreateThemeForm,
    CreateThemeWithSectionForm,
    CreateMessageForm,
)
from forum.models import (
    Theme,
    Message,
    Section,
)
from forum.utils import DataMixin
from forum.views_base import (
    ThemeListBase,
    MessagesListBase, HomePageBase,
)


class ShowAbout(DataMixin, TemplateView):
    template_name = "forum/about.html"
    title_page = "О себе"


class HomePage(HomePageBase):
    template_name = "forum/index.html"
    title_page = "Главная"


class ThemeList(ThemeListBase):
    template_name = "forum/theme_list.html"
    title_page = "Темы"

    def get_queryset(self):
        object_list = self.model.objects.all()
        return self._apply_filters_to_object_list(object_list)


class ThemesOnSectionList(ThemeListBase):
    template_name = "forum/themes_on_section.html"

    def get_queryset(self):
        object_list = self.model.objects.filter(
            section__pk=self.kwargs["section_id"]
        )
        return self._apply_filters_to_object_list(object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_id = self.kwargs["section_id"]
        title = Section.objects.get(pk=section_id).title
        return self.get_mixin_context(
            context,
            section_id=section_id,
            title=title,
        )


class MessagesOnThemeList(MessagesListBase):
    template_name = "forum/messages_on_theme.html"

    def get(self, *args, **kwargs):
        parent_id = self.request.GET.get("parent_id")
        if parent_id:
            base_url = reverse_lazy(
                "messages_on_theme",
                kwargs={
                    "theme_id": self.kwargs["theme_id"],
                    "section_id": self.kwargs["section_id"],
                },
            )
            all_messages = list(
                self.model.active.filter(
                    theme__pk=self.kwargs["theme_id"]
                ).values_list("pk", flat=True)
            )
            page = (all_messages.index(int(parent_id)) // self.paginate_by) + 1
            url = f"{base_url}?page={page}#message{parent_id}"
            return redirect(url)
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self._delete_message()
        return redirect(
            "messages_on_theme",
            theme_id=self.kwargs["theme_id"],
            section_id=self.kwargs["section_id"],
        )

    def get_queryset(self):
        object_list = self.model.active.filter(
            theme__pk=self.kwargs["theme_id"]
        )
        return self._apply_filters_to_object_list(object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        theme = get_object_or_404(Theme, pk=theme_id)
        title = theme.title
        return self.get_mixin_context(
            context,
            theme_id=theme_id,
            section_id=section_id,
            title=title,
        )


class MyMessagesList(MessagesListBase):
    template_name = "forum/my_messages.html"
    title_page = "Мои сообщения"

    def post(self, *args, **kwargs):
        self._delete_message()
        return redirect("my_messages")

    def get_queryset(self):
        object_list = self.model.active.filter(
            author=self.request.user,
        )
        return self._apply_filters_to_object_list(object_list)


class CreateMessage(LoginRequiredMixin, DataMixin, CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = "forum/create_message.html"
    title_page = "Новое сообщение"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = self.kwargs["theme_id"]
        theme = get_object_or_404(Theme, pk=theme_id)
        try:
            message_id = self.kwargs["message_id"]
            parent = Message.active.get(pk=message_id)
        except KeyError:
            parent = None
        return self.get_mixin_context(
            context,
            theme=theme,
            parent=parent,
        )

    def form_valid(self, form):
        context = self.get_context_data()
        theme = context["theme"]
        parent = context["parent"]
        form.instance.author = self.request.user
        form.instance.theme = theme
        if parent:
            form.instance.parent = parent
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


class CreateThemeWithSection(LoginRequiredMixin, DataMixin, CreateView):
    model = Theme
    form_class = CreateThemeWithSectionForm
    template_name = "forum/create_theme_with_section.html"
    title_page = "Новая тема"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_id = self.kwargs["section_id"]
        section = Section.objects.get(pk=section_id)
        return self.get_mixin_context(
            context,
            section=section,
        )

    def form_valid(self, form):
        context = self.get_context_data()
        section = context["section"]
        form.instance.author = self.request.user
        form.instance.section =section
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
