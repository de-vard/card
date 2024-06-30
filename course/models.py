from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from core.mixins import SlugMixin, TimestampMixin

User = get_user_model()


class Course(SlugMixin, TimestampMixin, models.Model):
    title = models.CharField(max_length=75, verbose_name='Название')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    students = models.ManyToManyField(
        User,
        through='RegisteredUsers',
        verbose_name='Записанные на курс студенты',
        related_name='registered_users'
    )
    users_liked = models.ManyToManyField(
        User,
        related_name='courses_liked',
        blank=True,
        verbose_name="лайки пользователей"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-created"]

    def __str__(self):
        return self.title


class RegisteredUsers(models.Model):
    """Промежуточная модель для регистрации пользователя на курс"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'

    def __str__(self):
        return f'{self.user} записался на курс: {self.course}'
