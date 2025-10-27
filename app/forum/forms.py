from django.forms import (
    ModelForm,
    ModelChoiceField,
    TextInput,
)
from django.forms.widgets import (
    Select,
    Textarea,
)

from forum.models import (
    Theme,
    Section,
    Message,
)


class CreateThemeForm(ModelForm):

    section = ModelChoiceField(
        queryset=Section.objects.all(),
        empty_label="--- Выберите раздел ---",
        widget=Select(attrs={
            'class': 'form-input my-border form-control',
        })
    )

    class Meta:
        model = Theme
        fields = [
            "section",
            "title",
        ]
        labels = {
            "section": "Раздел",
            "title": "Тема",
        }
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-input my-border form-control',
                'placeholder': 'Название темы'
            }),
        }


class CreateMessageForm(ModelForm):

    class Meta:
        model = Message
        fields = [
            "content",
        ]
        labels = {
            "content": "Сообщение",
        }
        widgets = {
            "content": Textarea(attrs={
                'class': 'form-input my-border form-control',
                'placeholder': 'Введите текст сообщения...'
            }),
        }