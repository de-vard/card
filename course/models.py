from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=75, verbose_name='Название')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    slug = models.SlugField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    users_liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses_liked',
        blank=True,
        verbose_name="лайки пользователей"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if self._state.adding:  # Проверяем, новый ли это объект
            self.slug = f"{self.title}-{self.created}".replace(' ', '')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


