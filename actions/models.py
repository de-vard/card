from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from core.mixins import TimestampMixin


class Action(TimestampMixin,models.Model):
    """Модель для отслеживания действий пользователя"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField('действие которое выполнил пользователь', max_length=255)
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
