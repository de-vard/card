from django.contrib.auth.models import AbstractUser
from django.db import models

from mixins.models import SlugMixin


class CustomUser(SlugMixin, AbstractUser):
    """Расширяем пользовательскую модель"""
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='users/%Y/%m/%d/', blank=True)
    slug = models.SlugField('Слаг', max_length=250, blank=True)
    following = models.ManyToManyField(
        'self',  # Указываем что взаимосвязь многие-ко-многим из модели User на саму себя
        through='Follow',  # указываем что нужно использовать конкретно-прикладную промежуточную модель
        related_name='followers',
        symmetrical=False  # В данном же случае устанавливается параметр symmetrical=False, чтобы определить не
        # отслеживание действий пользователя симметричную взаимосвязь (если я на вас подписываюсь, то это не
        # означает, что вы автоматически подписываетесь на меня)
    )

    def __str__(self):
        return self.first_name if self.first_name else self.username


class Follow(models.Model):
    """Промежуточная модель подписки на пользователя"""
    user_from = models.ForeignKey('user.CustomUser', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('user.CustomUser', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['-created']), ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} подписался на {self.user_to}'
