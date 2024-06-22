from django.contrib import admin
from lesson import models


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Уроки"""
    list_display = ('id', 'title', 'course')
    filter_horizontal = ['words']  # меняем виджет при выборе слов
