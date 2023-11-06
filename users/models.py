import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from slugify import slugify

from cards.models import Card
from config import settings


class CustomUser(AbstractUser):
    """Расширяем пользовательскую модель"""
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='users/%Y/%m/%d/', blank=True)
    slug = models.SlugField('Слаг', max_length=250, blank=True)
    following = models.ManyToManyField(
        'self',  # Указываем что взаимосвязь многие-ко-многим из модели User на саму себя
        through='Contact',  # указываем что нужно использовать конкретно-прикладную промежуточную модель
        related_name='followers',
        symmetrical=False,  # делаем связь не семеричной (если я на вас подписываюсь, то это не означает,
        # что вы автоматически подписываетесь на меня)
    )

    def __str__(self):
        if self.first_name:
            return f'{self.first_name}'
        return f'{self.username}'

    def get_absolute_url(self):
        return reverse('users:detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """ Автоматически генерировать поля slug на основе значения поля title
        """
        if not self.slug:
            self.slug = slugify(
                f'{self.username}-{self.first_name}-{uuid.uuid4()}'
            )

        super().save(*args, **kwargs)


class Contact(models.Model):
    """ Промежуточная модель для взаимосвязей пользователей"""
    user_from = models.ForeignKey(
        'users.CustomUser',
        related_name='rel_from_set',
        on_delete=models.CASCADE,
        verbose_name='пользователя, который подписывается на другого пользователя.'
    )
    user_to = models.ForeignKey(
        'users.CustomUser',
        related_name='rel_to_set',
        on_delete=models.CASCADE,
        verbose_name='пользователь, на которого подписываются'

    )

    created = models.DateTimeField('хранение времени взаимосвязи', auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created']), ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class Action(models.Model):
    """Модель для отслеживания действий пользователя"""
    user = models.ForeignKey('users.CustomUser', related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField('действие которое выполнил пользователь', max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(  # сообщает о модели, используемой для взаимосвязи
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)  # хранения первичного ключа связанного объекта
    target = GenericForeignKey('target_ct', 'target_id')  # GenericForeignKey - это специальный тип поля ForeignKey,

    # который позволяет создавать «универсальные» отношения с любой другой моделью

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']


