from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Расширяем пользовательскую модель"""
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='users/%Y/%m/%d/', blank=True)
    slug = models.SlugField('Слаг', max_length=250, blank=True)

    def __str__(self):
        return self.first_name if self.first_name else self.username

    def save(self, *args, **kwargs):
        if self._state.adding:  # Проверяем, новый ли это объект
            self.slug = f"{self.first_name}-{self.date_joined}"
        return super().save(*args, **kwargs)


class Contact(models.Model):
    user_from = models.ForeignKey('user.CustomUser', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('user.CustomUser', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField('хранение времени взаимосвязи', auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created']),]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} подписался на {self.user_to}'


user_model = get_user_model()  # получаем модель пользователя
# В модель User добавляем поле автоматически
# Метод add_to_class() моделей Django применяется для того, чтобы динамически подправлять модель User
user_model.add_to_class('following', models.ManyToManyField(
    'self',  # Указываем что взаимосвязь многие-ко-многим из модели User на саму себя
    through=Contact,  # указываем что нужно использовать конкретно-прикладную промежуточную модель
    related_name='followers',
    symmetrical=False  # В данном же случае устанавливается параметр symmetrical=False, чтобы определить не
    # Отслеживание действий пользователя симметричную взаимосвязь (если я на вас подписываюсь, то это не означает,
    # что вы автоматически подписываетесь на меня)
))
