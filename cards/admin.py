from django.contrib import admin
from cards.models import Card, WrongCards, Image
from django.utils.safestring import mark_safe


class WrongCardsInline(admin.TabularInline):
    model = WrongCards
    fields = ('mistake_in', 'error_text', 'author')
    extra = 0
    # TODO: Орзанизуй что бы автора в админке нельзя было менять


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('term', 'definition', 'card_have_wrong', 'slug', 'get_image',)
    list_editable = ('definition',)  # Быстрое редактирование
    readonly_fields = ('get_image',)  # Добавляем изображение
    prepopulated_fields = {'slug': ('term',)}  # автоматическое заполнение слага
    search_fields = ('term', 'definition',)  # Поиск
    exclude = ('author',)  # Уберем поле из админки
    inlines = [
        WrongCardsInline,
    ]

    def save_model(self, request, obj, form, change):
        """Получаем пользователя и устанавливаем его как автора"""
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_image(self, obj):
        """Получаем мини изображение или возвращаем что его нет"""
        if obj.image:
            return mark_safe(f'<img src={obj.image.photo.url} width="50" height="60">')
        else:
            return 'Фото отсутствует'

    def card_have_wrong(self, obj):
        """
            Возвращает есть ли в карточке ошибка
            Получаю доступ к связанным записям вторичной
            модели через related_name
        """
        if obj.wrong_cards.all():
            return 'Да'
        return 'Нет'

    card_have_wrong.short_description = 'Есть ли ошибка'  # Указываем название для короткого названия
    card_have_wrong.admin_order_field = 'wrong_cards'  # Добавляем сортировку при просмотре всех элементов
    get_image.short_description = 'Изображения'  # Указываем название мини изображения

    # fieldsets = наборы-полей
    fieldsets = (
        ("Текстовая Информация", {
            'description': 'Эти поля обязаны для каждой карточки',
            'fields': ('term', 'definition', 'transcription', 'slug')
        }),
        ('Медиа Файлы', {
            'classes': ('collapse',),  # для кнопки скрытия в админке
            'fields': (('image', 'get_image', 'audi'),)
        }),
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
