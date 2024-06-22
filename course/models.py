from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=75, verbose_name='Название')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    slug = models.SlugField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registered_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CourseRegistration',
        verbose_name='Записи на курс',
        related_name='registered_courses'
    )
    users_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses_liked',
        blank=True,
        verbose_name="лайки пользователей"
    )

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if self._state.adding:  # Проверяем, новый ли это объект
            self.slug = f"{self.title}-{self.created}".replace(' ', '')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


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
