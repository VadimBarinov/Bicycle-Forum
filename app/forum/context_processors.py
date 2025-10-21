from forum.utils import menu
from app import settings


def get_forum_context(request):
    return {
        'main_menu': menu,
        'default_profile': settings.DEFAULT_PROFILE_IMAGE,
    }
