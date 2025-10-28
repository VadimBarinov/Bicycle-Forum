from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import (
    Q,
    F,
    Value,
    CharField,
)
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
)

from forum.forms import (
    CreateThemeForm,
    CreateThemeWithSectionForm,
    CreateMessageForm,
)
from forum.models import (
    Theme,
    Message, Section,
)
from forum.utils import DataMixin


class ShowAbout(DataMixin, TemplateView):
    template_name = "forum/about.html"
    title_page = "О себе"


class HomePage(DataMixin, ListView):
    model = Section
    template_name = "forum/index.html"
    title_page = "Главная"
    context_object_name = "sections"
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        if query and query != "":
            params = {"query": query}
            base_url = reverse_lazy("theme_list")
            url = f"{base_url}?{urlencode(params)}"
            return redirect(url)
        return super().get(request, *args, **kwargs)


class ThemeList(DataMixin, ListView):
    model = Theme
    template_name = "forum/theme_list.html"
    title_page = "Темы"
    context_object_name = "themes"
    paginate_by = 10

    def get_queryset(self):
        object_list = Theme.objects.all()
        query = self.request.GET.get("query")
        is_ascending = self.request.GET.get("is_ascending")

        if query and query != "":
            object_list = object_list.annotate(
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

        if is_ascending:
            object_list = object_list.order_by("-pk")
        else:
            object_list = object_list.order_by("pk")

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        input_value = self.request.GET.get("query")
        ascending_value = self.request.GET.get("is_ascending")
        if ascending_value:
            is_ascending = False
        else:
            is_ascending = True

        return self.get_mixin_context(
            context,
            input_value=input_value,
            is_ascending=is_ascending,
        )


class ThemesOnSectionList(DataMixin, ListView):
    model = Theme
    template_name = "forum/themes_on_section.html"
    context_object_name = "themes"
    paginate_by = 10

    def get_queryset(self):
        object_list = Theme.objects.filter(
            section__pk=self.kwargs["section_id"]
        )
        query = self.request.GET.get("query")
        is_ascending = self.request.GET.get("is_ascending")

        if query and query != "":
            object_list = object_list.annotate(
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

        if is_ascending:
            object_list = object_list.order_by("-pk")
        else:
            object_list = object_list.order_by("pk")

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        input_value = self.request.GET.get("query")
        section_id = self.kwargs["section_id"]
        title = Section.objects.get(pk=section_id).title
        ascending_value = self.request.GET.get("is_ascending")
        if ascending_value:
            is_ascending = False
        else:
            is_ascending = True

        return self.get_mixin_context(
            context,
            input_value=input_value,
            is_ascending=is_ascending,
            section_id=section_id,
            title=title,
        )


class MessagesOnThemeList(DataMixin, ListView):
    model = Message
    template_name = "forum/messages_on_theme.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self):
        object_list = Message.objects.filter(
            theme__pk=self.kwargs["theme_id"]
        )
        query = self.request.GET.get("query")
        is_ascending = self.request.GET.get("is_ascending")

        if query and query != "":
            object_list = object_list.annotate(
                content_and_author=Concat(
                    F("content"),
                    Value(" "),
                    F("author__username"),
                    output_field=CharField(),
                )
            ).filter(
                Q(content_and_author__icontains=query)
            )

        if is_ascending:
            object_list = object_list.order_by("-pk")
        else:
            object_list = object_list.order_by("pk")

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        input_value = self.request.GET.get("query")
        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        title = Theme.objects.get(pk=theme_id).title
        ascending_value = self.request.GET.get("is_ascending")
        if ascending_value:
            is_ascending = False
        else:
            is_ascending = True

        return self.get_mixin_context(
            context,
            input_value=input_value,
            is_ascending=is_ascending,
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