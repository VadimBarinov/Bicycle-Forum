from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
)

from forum.forms import (
    SectionFilterForm,
    CreateThemeForm,
    CreateThemeWithSectionForm,
    CreateMessageForm,
)
from forum.models import (
    Theme,
    Message, Section,
)
from forum.utils import DataMixin
from forum.views_utils import (
    get_theme_list_with_query,
    get_message_list_with_query,
    check_click_ascending,
    sort_in_ascending_or_descending_order,
)


class ShowAbout(DataMixin, TemplateView):
    template_name = "forum/about.html"
    title_page = "О себе"


class HomePage(DataMixin, ListView):
    model = Section
    template_name = "forum/index.html"
    title_page = "Главная"
    context_object_name = "sections"
    paginate_by = 3

    section_filter_form = SectionFilterForm
    selected_sections = []

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        if query:
            params = {"query": query}
            base_url = reverse_lazy("theme_list")
            url = f"{base_url}?{urlencode(params)}"
            return redirect(url)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if "sections" in self.request.GET:
            form = SectionFilterForm(self.request.GET)
            if form.is_valid():
                selected_sections = form.cleaned_data["sections"]
                if selected_sections:
                    self.section_filter_form = form
                    self.selected_sections = [
                        section.pk for section in selected_sections
                    ]
                    print(self.selected_sections)
                    return selected_sections
        elif "reset_sections" in self.request.GET:
            self.section_filter_form = SectionFilterForm
            self.selected_sections = []
            return self.model.objects.all()
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            section_filter_form = self.section_filter_form,
            selected_sections = self.selected_sections,
        )


class ThemeList(DataMixin, ListView):
    model = Theme
    template_name = "forum/theme_list.html"
    title_page = "Темы"
    context_object_name = "themes"
    paginate_by = 10

    is_ascending = None
    query = None

    def get_queryset(self):
        object_list = self.model.objects.all()
        self.query = self.request.GET.get("query")
        object_list = get_theme_list_with_query(
            object_list,
            self.query,
        )
        self.is_ascending = check_click_ascending(self.request)
        object_list = sort_in_ascending_or_descending_order(
            object_list,
            self.is_ascending,
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            query=self.query,
            is_ascending=self.is_ascending,
        )


class ThemesOnSectionList(DataMixin, ListView):
    model = Theme
    template_name = "forum/themes_on_section.html"
    context_object_name = "themes"
    paginate_by = 10

    is_ascending = None
    query = None

    def get_queryset(self):
        object_list = self.model.objects.filter(
            section__pk=self.kwargs["section_id"]
        )
        self.query = self.request.GET.get("query")
        object_list = get_theme_list_with_query(
            object_list,
            self.query,
        )
        self.is_ascending = check_click_ascending(self.request)
        object_list = sort_in_ascending_or_descending_order(
            object_list,
            self.is_ascending,
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_id = self.kwargs["section_id"]
        title = Section.objects.get(pk=section_id).title
        return self.get_mixin_context(
            context,
            query=self.query,
            is_ascending=self.is_ascending,
            section_id=section_id,
            title=title,
        )


class MessagesOnThemeList(DataMixin, ListView):
    model = Message
    template_name = "forum/messages_on_theme.html"
    context_object_name = "messages"
    paginate_by = 10

    is_ascending = None
    query = None

    def get_queryset(self):
        object_list = self.model.active.filter(
            theme__pk=self.kwargs["theme_id"]
        )
        self.query = self.request.GET.get("query")
        object_list = get_message_list_with_query(
            object_list,
            self.query,
        )
        self.is_ascending = check_click_ascending(self.request)
        object_list = sort_in_ascending_or_descending_order(
            object_list,
            self.is_ascending,
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = self.kwargs["theme_id"]
        section_id = self.kwargs["section_id"]
        title = Theme.objects.get(pk=theme_id).title
        return self.get_mixin_context(
            context,
            query=self.query,
            is_ascending=self.is_ascending,
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