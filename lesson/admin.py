from django.contrib import admin
from lesson import models


# Register your models here.
@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Уроки"""
    list_display = ('id','title')
    filter_horizontal = ['words']  # меняем виджет при выборе слов


@admin.register(models.LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """Прогресс пользователя в уроках"""

    list_display = ('id', 'user', 'lesson',)
    filter_horizontal = ['cards']  # меняем виджет при выборе слов

