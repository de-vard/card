from django.contrib import admin
from lesson import models


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Уроки"""
    list_display = ('id', 'title', 'course')
    exclude = ('slug',)  # Исключаем поле slug из формы админки
