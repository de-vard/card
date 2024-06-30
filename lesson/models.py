from django.db import models
from django.urls import reverse

from core.mixins import TimestampMixin
from course.models import Course


class Lesson(TimestampMixin, models.Model):
    """Модель урока"""
    title = models.CharField(max_length=75, verbose_name='Название')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курсы')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('lesson:detail', args=[self.pk])

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-created']
