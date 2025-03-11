from rest_framework import serializers
from rest_framework.reverse import reverse

from course.models import Course
from flashcard.serializers import FlashCardSerializer
from lesson.models import Lesson


class LessonSerializerList(serializers.ModelSerializer):
    """Сериализатор для уроков, который включает вложенные карточки"""

    num_flashcard = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return reverse('lesson-detail', args=(obj.pk,))

    def get_num_flashcard(self, obj):
        return obj.flashcards.count()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'num_flashcard', 'absolute_url')


class LessonSerializerDetails(serializers.ModelSerializer):
    """Сериализатор для уроков, который включает вложенные карточки"""
    flashcards = FlashCardSerializer(many=True, read_only=True)
    belongs_course = serializers.SlugRelatedField(slug_field='title', source='course', read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'belongs_course', 'title', 'flashcards', 'course')
