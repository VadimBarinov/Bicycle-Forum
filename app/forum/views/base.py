from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
)

from forum.forms import (
    SectionFilterForm,
    CreateMessageForm,
    CreateThemeForm,
)
from forum.models import (
    Theme,
    Message,
    Section,
)
from forum.utils import DataMixin
from .utils import (
    redirect_from_home_to_theme_list,
    get_theme_list_by_query,
    check_click_ascending,
    sort_in_ascending_or_descending_order,
    get_message_list_by_query,
    delete_message,
)


class ShowAboutBase(DataMixin, TemplateView):
    pass


class HomePageBase(DataMixin, ListView):
    model = Section
    context_object_name = "sections"
    paginate_by = 3

    section_filter_form = SectionFilterForm
    selected_sections = []

    def _get_selected_sections(self) -> QuerySet:
        if "sections" in self.request.GET:
            form = self.section_filter_form(self.request.GET)
            if form.is_valid():
                selected_sections = form.cleaned_data["sections"]
                if selected_sections:
                    self.section_filter_form = form
                    self.selected_sections = [
                        section.pk for section in selected_sections
                    ]
                    return selected_sections
        elif "reset_sections" in self.request.GET:
            self.section_filter_form = SectionFilterForm
            self.selected_sections = []
            return self.model.objects.all()
        return self.model.objects.all()

    def get_queryset(self):
        return self._get_selected_sections()

    def get(self, *args, **kwargs):
        query = self.request.GET.get("query")
        if query:
            return redirect_from_home_to_theme_list(query)
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            section_filter_form = self.section_filter_form,
            selected_sections = self.selected_sections,
        )


class ThemeListBase(DataMixin, ListView):
    model = Theme
    context_object_name = "themes"
    paginate_by = 10

    is_ascending = None
    query = None
    all_themes_count = 0

    def _apply_filters_to_object_list(
            self,
            object_list: QuerySet,
    ) -> QuerySet:
        self.query = self.request.GET.get("query")
        object_list = get_theme_list_by_query(
            object_list,
            self.query,
        )
        self.is_ascending = check_click_ascending(self.request)
        object_list = sort_in_ascending_or_descending_order(
            object_list,
            self.is_ascending,
        )
        self.all_themes_count = len(object_list)
        return object_list

    def get_queryset(self):
        object_list = self.model.objects.all()
        return self._apply_filters_to_object_list(object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            query=self.query,
            is_ascending=self.is_ascending,
            all_themes_count = self.all_themes_count,
        )


class MessagesListBase(DataMixin, ListView):
    model = Message
    context_object_name = "messages"
    paginate_by = 10

    is_ascending = None
    query = None
    all_messages_count = 0

    def _apply_filters_to_object_list(
            self,
            object_list: QuerySet,
    ) -> QuerySet:
        self.query = self.request.GET.get("query")
        object_list = get_message_list_by_query(
            object_list,
            self.query,
        )
        self.is_ascending = check_click_ascending(self.request)
        object_list = sort_in_ascending_or_descending_order(
            object_list,
            self.is_ascending,
        )
        self.all_messages_count = len(object_list)
        return object_list

    def _delete_message(self) -> None:
        message_delete_id = self.request.POST.get("message_delete_id")
        if message_delete_id:
            delete_message(
                user=self.request.user,
                message_delete_id=message_delete_id,
            )

    def get_queryset(self):
        object_list = self.model.active.all()
        return self._apply_filters_to_object_list(object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            query=self.query,
            is_ascending=self.is_ascending,
            all_messages_count=self.all_messages_count,
        )

class CreateMessageBase(LoginRequiredMixin, DataMixin, CreateView):
    model = Message
    form_class = CreateMessageForm

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

class CreateThemeBase(LoginRequiredMixin, DataMixin, CreateView):
    model = Theme
    form_class = CreateThemeForm

    def _instance_author(self, form):
        form.instance.author = self.request.user
        return form

    def form_valid(self, form):
        return super().form_valid(
            self._instance_author(form)
        )

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