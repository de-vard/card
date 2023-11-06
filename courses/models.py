from django.db import models
from django.conf import settings
from django.urls import reverse

from .utils import generate_slug


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Course(models.Model):
    """Модель Курса"""
    CHOICE = (
        ('a', 'Легкий'),
        ('b', 'Средний'),
        ('с', 'Сложный'),
    )
    level = models.CharField(choices=CHOICE, max_length=1, verbose_name='Уровень сложности', blank=True)
    title = models.CharField(max_length=75, verbose_name='Название')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего редактирования', auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Теги')
    slug = models.SlugField('Слаг', max_length=250, unique=True)
    registrations = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CourseRegistration',
        verbose_name='Записи на курс',
        related_name='registered_courses'
    )

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('course:detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """ Автоматически генерировать поля slug на основе значения поля title
        """
        if not self.slug:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-created']),
        ]


class CourseRegistration(models.Model):
    """ Промежуточная модель для записи пользователей на курс"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateTimeField('Дата записи', auto_now_add=True)

    class Meta:
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курсы"

    def __str__(self):
        return f'{self.user} записался на курс: {self.course}'
