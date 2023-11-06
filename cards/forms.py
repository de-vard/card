from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import WrongCards, Card


class WrongCardsForm(ModelForm):
    """Форма для создания сообщения об ошибке слова"""

    class Meta:
        model = WrongCards
        fields = ['mistake_in', 'error_text', ]


class CardForm(forms.ModelForm):
    """Форма для создания карточек"""
    term = forms.CharField(required=True)
    definition = forms.CharField(required=True)

    class Meta:
        model = Card
        fields = ['term', 'transcription', 'definition', 'image']


# Используем modelformset_factory для формирования нескольких карточек на одной странице
CardFormSet = modelformset_factory(
    Card,
    form=CardForm,
    fields=['term', 'transcription', 'definition', 'image'],
    extra=1,
    can_delete=True  # Если True, то Django будет вставлять булево поле для каждой формы, которая будет
    # прорисовываться в виде флажка. Этим обеспечивается возможность помечать объекты, которые требуется удалить
)
