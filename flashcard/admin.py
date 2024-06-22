from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image, FlashCard


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image')  # Поля для отображения в списке
    search_fields = ('title',)  # Поля для поиска
    list_filter = ('title',)  # Поля для фильтрации

    def get_image(self, obj):
        """Получаем мини изображение или возвращаем что его нет"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="60" />')
        else:
            return 'Фото отсутствует'

    get_image.short_description = 'Изображение'  # Указываем название мини изображения
    readonly_fields = ('get_image',)  # Делаем поле только для чтения


@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('english_word', 'russian_word', 'transcription', 'get_image')  # Поля для отображения в списке
    search_fields = ('english_word', 'russian_word', 'transcription')  # Поля для поиска
    exclude = ('author',)  # Уберем поле из админки
    readonly_fields = ('get_image', 'created', 'updated')  # Добавляем изображение как только для чтения

    def get_image(self, obj):
        """Получаем мини изображение или возвращаем что его нет"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.photo.url}" width="50" height="60" />')
        else:
            return 'Фото отсутствует'

    get_image.short_description = 'Изображение'  # Указываем название мини изображения

    fieldsets = (
        (None, {
            'fields': ('english_word', 'russian_word', 'transcription')
        }),
        ('Media', {
            'fields': ('image', 'sound', 'get_image')
        }),
        ('Dates', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),  # для кнопки скрытия в админке
        }),
    )
