from django.db import models


class TimestampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:  # Проверяем, новый ли это объект
            self.slug = f"{self.title}-{self.created}".replace(' ', '')
        return super().save(*args, **kwargs)
