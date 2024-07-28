from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from flashcard.serializers import FlashCardSerializer
from lesson.permissions import IsAuthenticatedAndEnrolled, IsAuthor
from lesson.serializers import LessonSerializerList, LessonSerializerDetails

from flashcard.models import FlashCard, LearnerFlashCard
from lesson.models import Lesson


# Todo: проверь код на разрешения, создай тысты для тестирования кода,
#  код копировался из курсов, проверь все ли подогнал для уроков

class LessonListAPIView(generics.ListAPIView):
    """Список уроков"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializerList


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотер уроков без редактирования"""
    lookup_field = "id"
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticatedAndEnrolled]
    serializer_class = LessonSerializerDetails


class LessonRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование урока"""
    lookup_field = 'id'
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = LessonSerializerDetails


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializerDetails


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    lookup_field = 'id'
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class LearnFlashcards(APIView):
    """Список карточек в уроке, для изучения его"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    @staticmethod
    def get_learner_flashcards(lesson, user):
        """Вспомогательная функция для получения карточек для изучения."""
        learner_flashcards = FlashCard.objects.filter(
            lesson=lesson,
            learnerflashcard__user=user,
            learnerflashcard__learned_word=False
        )
        return learner_flashcards

    def get(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        user = request.user

        learner_flashcards = self.get_learner_flashcards(lesson, user)
        serializer = FlashCardSerializer(learner_flashcards, many=True)
        return Response(serializer.data)


class ResetResultLesson(APIView):
    """Сброс результавом урока, обнуления выучиных слов в уроке"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        user = request.user

        # Получаем все записи LearnerFlashCard для данного урока и пользователя
        learner_flashcards = LearnerFlashCard.objects.filter(
            flashcard__lesson=lesson,
            user=user
        )

        # Обновляем поле learned_word на False
        learner_flashcards.update(learned_word=False)

        # Перенаправление на метод learn_flashcards
        return redirect('lesson-learn', pk=pk)
