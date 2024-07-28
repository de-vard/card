from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from mixins.models import TimestampSlugMixin

User = get_user_model()


class Course(TimestampSlugMixin, models.Model):
    title = models.CharField(max_length=75, verbose_name='Название')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    students = models.ManyToManyField(
        User,
        through='RegisteredUsers',
        verbose_name='Записанные на курс студенты',
        related_name='registered_users'
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
    liked = models.BooleanField(default=False, verbose_name='Лайкнул курс')
    disliked = models.BooleanField(default=False, verbose_name='Дизлайкнул курс')

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'

    def save(self, *args, **kwargs):
        if self.liked and self.disliked:
            # Если лайк и дизлайк установлены одновременно, пропустить сохранение
            return  # Не сохранять объект

        # Если лайк установлен в True, снимаем дизлайк
        if self.liked:
            self.disliked = False

        # Если дизлайк установлен в True, снимаем лайк
        if self.disliked:
            self.liked = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} записался на курс: {self.course}'
