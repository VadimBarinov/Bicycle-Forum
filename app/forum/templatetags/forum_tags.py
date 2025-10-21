import random
from django import template


# регистрация новых тегов
register = template.Library()


@register.filter
def find_image(image_url):
    try:
        if (image_url and image_url.file):
            return True
    except FileNotFoundError:
        return False


@register.simple_tag
def my_range(first, second):
    return list(range(first, second))


@register.filter
def get_value_from_dict(dict_data, key):
    return dict_data.get(key)
