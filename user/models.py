import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

from mixins.models import SlugMixin, TimestampSlugMixin


class UserManager(BaseUserManager):

    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an email.')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)

        # Аргумент using указывает, какую базу данных использовать для сохранения объекта. self._db обычно ссылается
        # на базу данных, к которой подключён текущий менеджер модели.
        user.save(using=self._db)

        return user


class CustomUser(SlugMixin, AbstractUser):
    """Расширяем пользовательскую модель"""
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField('Имя пользователя', db_index=True, max_length=255, unique=True)
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    email = models.EmailField('email', db_index=True, unique=True)
    is_active = models.BooleanField('Активный пользователь', default=True)
    bio = models.TextField('Биография', blank=True)
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

    objects = UserManager()  # Менеджер модели, который будет управлять созданием и обработкой пользователей

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
