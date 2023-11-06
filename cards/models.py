

from django.core import validators
from django.db import models
from django.conf import settings

# TODO:Добавь идексацию полей, коорые будут использываться в поисках и сортировках
from django.urls import reverse

from courses.utils import generate_slug


class WrongCards(models.Model):
    """Карточки с ошибками"""
    CHOICE = ((None, 'Выберите в чем ошибка'), ('a', 'терминe'), ('b', 'определение'), ('c', 'произношение'))
    mistake_in = models.CharField('Ошибка в', choices=CHOICE, max_length=3)
    card = models.ForeignKey('Card', on_delete=models.CASCADE, verbose_name='Ошибка', related_name='wrong_cards')
    error_text = models.TextField('Подробнее об ошибки')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.error_text


class Image(models.Model):
    """Изображения"""
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    title = models.CharField(max_length=50, verbose_name='Название')
    related_words = models.TextField('Связанные слова', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Card(models.Model):
    """Карточки слов"""

    term = models.CharField('Термин', max_length=100)
    transcription = models.CharField('Транскрипция', max_length=100, blank=True)
    definition = models.CharField('Определение', max_length=100)
    slug = models.SlugField('Слаг', max_length=250, unique=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего редактирования', auto_now=True)
    audi = models.FileField(
        upload_to='audi/%Y/%m/%d',
        verbose_name='Произношение',
        blank=True,
        validators=[validators.RegexValidator(regex=".mp3")],
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Фото'
    )

    def __str__(self):
        return f'{self.term} - {self.definition}'

    def get_absolute_url(self):
        return reverse('card:detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """ Автоматически генерировать поля slug на основе значения поля term"""
        if not self.slug:
            self.slug = generate_slug(self.term)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Карточку"
        verbose_name_plural = "Карточки"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['term']),
            models.Index(fields=['definition']),
        ]
