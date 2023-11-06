from django import forms
from .models import Lesson


class LessonCreationForm(forms.ModelForm):
    """Форма создания урока"""
    title = forms.CharField(label='Название урока')

    class Meta:
        model = Lesson
        fields = ['title', ]
