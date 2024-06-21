from django.core.validators import FileExtensionValidator
from django.db import models


class Image(models.Model):
    """Изображения"""
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title


class FlashCard(models.Model):
    english_word = models.CharField(max_length=100, verbose_name='Английское слово')
    russian_word = models.CharField(max_length=100, verbose_name='Русское слово')
    transcription = models.CharField(max_length=100, verbose_name='Транскрипция')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    sound = models.FileField(
        upload_to='audi/%Y/%m/%d',
        verbose_name='Аудиофайл',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.russian_word
