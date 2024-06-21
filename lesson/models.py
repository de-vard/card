from django.db import models
from django.urls import reverse

from course.models import Course
from flashcard.models import FlashCard


class Lesson(models.Model):
    """Модель урока"""
    title = models.CharField(max_length=75, verbose_name='Название')
    words = models.ManyToManyField(FlashCard, verbose_name='Слова')
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
