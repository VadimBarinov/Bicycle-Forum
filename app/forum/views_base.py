from django.db.models import QuerySet
from django.views.generic import ListView

from forum.forms import SectionFilterForm
from forum.models import (
    Theme,
    Message,
    Section,
)
from forum.utils import DataMixin
from forum.views_utils import (
    redirect_from_home_to_theme_list,
    get_theme_list_by_query,
    check_click_ascending,
    sort_in_ascending_or_descending_order,
    get_message_list_by_query,
    delete_message,
)


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
            redirect_from_home_to_theme_list(query)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            query=self.query,
            is_ascending=self.is_ascending,
            all_messages_count=self.all_messages_count,
        )