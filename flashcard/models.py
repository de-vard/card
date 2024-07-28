from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models


from lesson.models import Lesson
from mixins.models import TimestampSlugMixin

User = get_user_model()


class Image(models.Model):
    """Изображения"""
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title


class FlashCard(TimestampSlugMixin, models.Model):
    english_word = models.CharField(max_length=100, verbose_name='Английское слово')
    russian_word = models.CharField(max_length=100, verbose_name='Русское слово')
    transcription = models.CharField(max_length=100, verbose_name='Транскрипция')
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='flashcards',
        verbose_name='Урок'
    )
    learner = models.ManyToManyField(
        User,
        through='LearnerFlashCard',
        verbose_name='Пользователи изучающие карточки',
        related_name='learner_flashcard',

    )
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


class LearnerFlashCard(models.Model):
    """Промежуточная модель для проверки пользователя изучил ли он карточку"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE, verbose_name='Карточка')
    learned_word = models.BooleanField(default=False, verbose_name='Изучено ли слово')

    class Meta:
        unique_together = ('user', 'flashcard')
        verbose_name = 'Статус изучения карточки'
        verbose_name_plural = 'Статусы изучения карточек'

    def __str__(self):
        return f"{self.user} - {self.flashcard} - {'Изучено' if self.learned_word else 'Не изучено'}"
