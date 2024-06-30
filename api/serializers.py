from django.contrib.auth import get_user_model
from rest_framework import serializers

from course.models import Course
from flashcard.models import FlashCard, Image
from lesson.models import Lesson

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Используется для отображения информации о пользователях."""

    class Meta:
        model = User
        fields = ('username',)


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений"""

    class Meta:
        model = Image
        fields = ('photo',)


class FlashCardSerializer(serializers.ModelSerializer):
    """Сериализатор для карточек, в котором описаны все необходимые поля."""
    learner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Заполняем поле учиника  автоматически
    set_image = ImageSerializer(source='image', read_only=True)

    # Todo: Не Забудь, реализовать что бы карточки подвязывались к уроку в котором их создали
    #  убрать дублирующий поле изображения
    class Meta:
        model = FlashCard
        fields = ('english_word', 'russian_word', 'transcription', 'set_image', 'image', 'sound', 'learner')


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков, который включает вложенные карточки"""
    flashcards = FlashCardSerializer(many=True, read_only=True)
    belongs_course = serializers.SlugRelatedField(slug_field='title', source='course', read_only=True)

    # Todo: Не Забудь, реализовать выбор по курсам, но чтобы по умолчанию был курс в который провалился пользователь,
    #  убрать дублирующий поле курсов
    class Meta:
        model = Lesson
        fields = ('belongs_course', 'course', 'title', 'flashcards',)


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор для курсов, который автоматически заполняет поле автора текущим пользователем.
        Включает информацию о студентах и уроках, а также детализированную информацию об авторе.
    """
    # Заполняем поле автора курса автоматически
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    students = UserSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    # Используется для отображения информации об авторе курса Поле source указывает, какое поле модели использовать
    # для заполнения данных в данном поле сериализатора, read_only=True Указывает, что это поле доступно только для
    # чтения. Оно не будет включено в данные, передаваемые при создании или обновлении курса.
    course_author = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Course
        fields = ('title', 'course_author', 'author', 'created', 'lessons', 'students')
