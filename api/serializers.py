from django.contrib.auth import get_user_model
from rest_framework import serializers

from course.models import Course
from flashcard.models import FlashCard
from lesson.models import Lesson

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ('id', 'english_word', 'russian_word', 'transcription', 'image', 'sound')


class LessonSerializer(serializers.ModelSerializer):
    words = FlashCardSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'words')


class CourseSerializer(serializers.ModelSerializer):
    students = UserSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('title', 'author', 'created', 'lessons', 'students')
