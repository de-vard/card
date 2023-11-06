from django.db import models
from django.urls import reverse

from cards.models import Card
from courses.models import Course

from django.conf import settings


class Lesson(models.Model):
    """Модель урока"""
    title = models.CharField(max_length=75, verbose_name='Название')
    words = models.ManyToManyField(Card, verbose_name='Слова')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курсы')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего редактирования', auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('lesson:detail', args=[self.pk])

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-created']


class LessonProgress(models.Model):
    """Модель прогресса пользователя"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Прогресс пользователя')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    cards = models.ManyToManyField(Card, blank=True)

    def __str__(self):
        return f'Прогресс урока: {self.lesson.title}'

    class Meta:
        verbose_name = "Прогресс урока"
        verbose_name_plural = "Прогресс уроков"
