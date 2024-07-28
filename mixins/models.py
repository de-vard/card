import random
import string
from datetime import datetime

from django.db import models


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    @staticmethod
    def generate_random_string(length=9):
        characters = string.ascii_letters + string.digits  # латинские буквы (верхнего и нижнего регистра) и цифры
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    @staticmethod
    def get_current_time():
        now = datetime.now()
        date = [now.second, now.minute, now.hour, now.day, now.month, now.year]
        return ''.join(str(i) for i in date)

    def save(self, *args, **kwargs):
        if self._state.adding:  # Проверяем, новый ли это объект
            self.slug = self.generate_random_string() + self.get_current_time()
        return super().save(*args, **kwargs)


class TimestampSlugMixin(SlugMixin):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
