from django.db.models import (
    F,
    Value,
    CharField,
    Q,
)
from django.db.models.functions import Concat

from forum.models import Message


def get_theme_list_with_query(
        object_list,
        query,
):
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
    return object_list


def get_message_list_with_query(
        object_list,
        query,
):
    if query and query != "":
        object_list = object_list.filter(
            Q(content__icontains=query)
        )
    return object_list


def check_click_ascending(request):
    if "click_ascending" in request.GET:
        is_ascending = not bool(request.GET.get("is_ascending"))
    else:
        is_ascending = bool(request.GET.get("is_ascending"))
    return is_ascending


def sort_in_ascending_or_descending_order(
        object_list,
        is_ascending,
):
    if is_ascending:
        object_list = object_list.order_by("-pk")
    else:
        object_list = object_list.order_by("pk")
    return object_list


def delete_message(user, message_delete_id):
    if user.is_authenticated:
        found_message = Message.active.get(
            Q(author__pk=user.pk) & Q(pk=message_delete_id)
        )
        found_message.deactivate_message()