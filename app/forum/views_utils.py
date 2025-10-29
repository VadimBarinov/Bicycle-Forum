from django.db.models import (
    F,
    Value,
    CharField,
    Q,
)
from django.db.models.functions import Concat


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


def sort_in_ascending_or_descending_order(
        object_list,
        is_ascending,
):
    if is_ascending:
        object_list = object_list.order_by("-pk")
    else:
        object_list = object_list.order_by("pk")
    return object_list