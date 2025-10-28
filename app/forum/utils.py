menu = [
    {
        "title": "Главная",
        "url": "home",
    },
    {
        "title": "Темы",
        "url": "theme_list",
    },
    {
        'title': 'О себе',
        'url': 'about',
    },
]


class DataMixin:

    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

    @staticmethod
    def get_mixin_context(context, **kwargs):
        context.update(kwargs)
        return context
