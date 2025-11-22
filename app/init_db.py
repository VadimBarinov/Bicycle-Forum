import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django.contrib.auth import get_user_model
from forum.models import (
    Section,
    Theme,
    Message,
)
from app.settings import (
    SUPERUSER_USERNAME,
    SUPERUSER_PASSWORD,
    SUPERUSER_EMAIL,
    SUPERUSER_PHOTO,
)


def create_super_admin():
    if not get_user_model().objects.filter(username="root").exists():
        get_user_model().objects.create_superuser(
            username=SUPERUSER_USERNAME,
            password=SUPERUSER_PASSWORD,
            email=SUPERUSER_EMAIL,
            photo=SUPERUSER_PHOTO,
        )


def create_test_users():
    get_user_model().objects.create_user(
        username="user1",
        password="user1qwerty",
        email="user1@mail.com",
        photo="users/2025/11/22/me.jpg",
    )
    get_user_model().objects.create_user(
        username="user2",
        password="user2qwerty",
        email="user2@mail.com",
        photo="users/2025/11/22/BlueCity.png",
    )


def create_test_sections():
    sections_list = [
        Section(title="Выбор велосипеда", created_at="2025-10-24 17:55:14.246043+04"),
        Section(title="Безопасность и здоровье", created_at="2025-10-24 17:55:41.296076+04"),
        Section(title="Юмор", created_at="2025-10-24 17:56:09.332636+04"),
        Section(title="Регионы", created_at="2025-10-24 17:56:25.853327+04"),
        Section(title="Другое", created_at="2025-10-24 21:06:43.824319+04"),
        Section(title="Новости", created_at="2025-10-24 17:52:42.145041+04"),
        Section(title="Техника", created_at="2025-10-24 17:54:46.06704+04"),
        Section(title="Стили катания", created_at="2025-10-24 17:56:30.470895+04"),
    ]
    Section.objects.bulk_create(sections_list)


def create_test_themes():
    themes_list = [
        Theme(
            title="Выбираем покрышки для туринга",
            created_at="2025-10-24 18:00:52.935+04",
            author_id=1,
            section_id=1,
        ),
        Theme(
            title="Какие-то новости",
            created_at="2025-11-19 21:15:58.644953+04",
            author_id=2,
            section_id=1,
        ),
        Theme(
            title="Выбор велосипеда: вопрос-ответ, быстрые консультации",
            created_at="2025-11-21 22:28:47.726057+04",
            author_id=3,
            section_id=3,
        ),
        Theme(
            title="Проблема коленей и как ее избежать",
            created_at="2025-10-27 09:42:36.258316+04",
            author_id=1,
            section_id=4,
        ),
    ]

    Theme.objects.bulk_create(themes_list)


def create_test_messages():
    messages_list = [
        Message(
            content=(
                "Встал остро вопрос покупки новой покрышки, размерность в заголовке (либо 28х1 5/8, либо 700х40С). Вопрос был задан мужику по имени Поиск, но мужик ясности не внес, пробурчав что-то невнятное по поводу того, что все нормальные люди на 27.5, 29 или 26 катают и вообще, надо было не выпендриваться и МТБ покупать.\n"
                "Дык вот хочу спросить у честного народа: даст кто наводку на дельные покрышки для гибрида указанной выше размерности? Штатные стоят Kenda какие-то там, но как-то меня не впечатлило то, что корд на задней покрышке начал в одном месте расходиться, в результате чего я получил расколбас вела на гладком асфальте посредством бодрящих ритмичных пинков по пятой точке. Так что хотел бы попробовать другую какую марку (но только не Сунь Хрен В Чай - Вынь, Пей Сам, ну, вы понимаете), но своей размерности как-то толком не нашел. Может, кто подскажет чего? Заранее спасибо"
            ),
            created_at="2025-11-22 09:21:48.302 +0400",
            author_id=1,
            theme_id=1,
        ),
        Message(
            content=(
                "Бери любую подходящую покрышку на вкус в размерностях 700х32 / 700х35 / 700х37 / 700х42 Conti / Michelin / Schwalbe"
            ),
            created_at="2025-11-22 09:22:53.733 +0400",
            author_id=3,
            parent_id=1,
            theme_id=1,
        ),
        Message(
            content=(
                "Continental Tour Ride 28x1.60 (42-622)"
            ),
            created_at="2025-11-22 09:23:08.149 +0400",
            author_id=3,
            theme_id=1,
        ),
        Message(
            content=(
                "Спасибо за совет!"
            ),
            created_at="2025-11-22 09:23:26.483 +0400",
            parent_id=3,
            author_id=1,
            theme_id=1,
        ),
        Message(
            content=(
                "Компания Shimano представила инновационную систему крепления CL-MT001, совместимую со стандартом SPD (Shimano Pedaling Dynamics). Новинка отличается от классических шипов SM-SH51, используемых с 1995 года, уникальной конической конструкцией, позволяющей соединяться с педалью под различными углами.\n\n"
                "В отличие от традиционных креплений, требующих входа в педаль строго передней частью шипа (носком вперёд), CL-MT001 обеспечивает три варианта соединения: передней частью, задней частью (пяткой вперёд) или прямым нажатием сверху. Это значительно упрощает процесс фиксации ноги на педали, особенно в ситуациях, требующих быстрого возвращения в седло после спешивания."
            ),
            created_at="2025-11-22 09:23:58.621 +0400",
            author_id=1,
            theme_id=2,
        ),
        Message(
            content=(
                "Закруглили носик в передней внешней стороны?"
                "Можно свои шипы подточить"
            ),
            created_at="2025-11-22 09:24:15.984 +0400",
            parent_id=5,
            author_id=2,
            theme_id=2,
        ),
        Message(
            content=(
                "Помогите с выбором. В общем цель покупки велосипеда длительные путешествия(хочу доехать до Сиднея на велосипеде, мечта идиота как говорится) Вобщем нужен велосипед как можно более надежен с возможностью перевозить багаж нагруженный 15-20кг. Мой рост составляет 1,76м, по цене думаю не дороже 1000$ можно дешевле или чуть дороже, если есть смысл. Пока остановился на таких вариантах\n\n"
                "1) Bergamont Helix 9.0 http://veliki.com.ua/goods_Bergamont_Helix_9_0.htm (не знаю если смысл переплачивать или стоит обратить внимание на Helix 7.0)\n"
                "2) Bergamont Helix 7.0 http://veliki.com.ua/goods_Bergamont_Helix_7_0.htm\n"
                "3) Ghost Panamao X 6 http://www.moyo.ua/velosiped-ghost-p...te-blue-l-2015\n"
                "4) Lapierre Cross 300 https://f.ua/lapierre/cross-300-2016...-65605600.html\n"
                "5) Apollo ASPIRE 40 http://veliki.com.ua/goods_Apollo_ASPIRE_40.htm\n"
                "6) PRIDE XC-29 PRO 1.0 http://www.pridebikes.com/pride-xc-29-pro-1-0"
            ),
            created_at="2025-11-22 09:24:41.584 +0400",
            author_id=2,
            theme_id=3,
        ),
        Message(
            content=(
                "Никаких амовилок и гидравлических тормозов. В идеале - Surly Cross Check или Long Haul Trucker"
            ),
            created_at="2025-11-22 09:25:00.547 +0400",
            parent_id=7,
            author_id=3,
            theme_id=3,
        ),
        Message(
            content=(
                "RedRojer\n\n"
                "1. нет, слишком высокая и короткая рама\n"
                "2. тоже самое\n"
                "3. ваш размер М\n"
                "4. ваш размер 51 (по ссылке 56)\n"
                "5. ваш размер М (по ссылке С)\n"
                "6. нет, слишком длинный"
            ),
            created_at="2025-11-22 09:25:10.855 +0400",
            parent_id=7,
            author_id=3,
            theme_id=3,
        ),
        Message(
            content=(
                "Да ничем тут не поможешь. Профилактика только."
            ),
            created_at="2025-11-22 09:25:28.649 +0400",
            author_id=3,
            theme_id=4,
        ),
        Message(
            content=(
                "А как же наколенники?"
            ),
            created_at="2025-11-22 09:25:54.240 +0400",
            parent_id=10,
            author_id=1,
            theme_id=4,
        ),
    ]

    Message.objects.bulk_create(messages_list)


def main():
    create_super_admin()
    create_test_users()
    create_test_sections()
    create_test_themes()
    create_test_messages()


if __name__ == '__main__':
    main()