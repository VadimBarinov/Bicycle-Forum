from urllib.parse import urlencode

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import (
    F,
    Value,
    CharField,
    Q,
    QuerySet,
)
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy

from forum.models import Message


def redirect_from_home_to_theme_list(
        query: str,
) -> HttpResponseRedirect:
    params = {"query": query}
    base_url = reverse_lazy("theme_list")
    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)


def get_theme_list_by_query(
        object_list: QuerySet,
        query: str,
) -> QuerySet:
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


def get_message_list_by_query(
        object_list: QuerySet,
        query: str,
) -> QuerySet:
    if query and query != "":
        object_list = object_list.filter(
            Q(content__icontains=query)
        )
    return object_list


def check_click_ascending(
        request: HttpRequest,
) -> bool:
    if "click_ascending" in request.GET:
        is_ascending = not bool(request.GET.get("is_ascending"))
    else:
        is_ascending = bool(request.GET.get("is_ascending"))
    return is_ascending


def sort_in_ascending_or_descending_order(
        object_list: QuerySet,
        is_ascending: bool,
) -> QuerySet:
    if is_ascending:
        object_list = object_list.order_by("-pk")
    else:
        object_list = object_list.order_by("pk")
    return object_list


def delete_message(
        user: AbstractBaseUser,
        message_delete_id: str,
) -> None:
    if user.is_authenticated:
        found_message = Message.active.get(
            Q(author__pk=user.pk) & Q(pk=message_delete_id)
        )
        found_message.deactivate_message()