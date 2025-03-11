from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from course.models import Course
from flashcard.serializers import FlashCardSerializer
from lesson.permissions import IsAuthenticatedAndEnrolled, IsAuthor
from lesson.serializers import LessonSerializerList, LessonSerializerDetails

from flashcard.models import FlashCard, LearnerFlashCard
from lesson.models import Lesson


class LessonListAPIView(generics.ListAPIView):
    """Список уроков"""
    http_method_names = ["get"]
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializerList


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотер уроков без редактирования"""
    lookup_field = "id"
    http_method_names = ["get"]
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializerDetails


class LessonRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование урока"""
    lookup_field = 'id'
    http_method_names = ["put"]
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]
    serializer_class = LessonSerializerDetails


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока"""
    http_method_names = ["post"]
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticatedAndEnrolled, IsAuthor]
    serializer_class = LessonSerializerDetails

    def perform_create(self, serializer):
        """
        Этот метод вызывается при создании нового урока. Он выполняет проверки:
        1. Проверяет, что курс существует.
        2. Проверяет, что текущий пользователь является владельцем курса.

        Если проверки прошли успешно, сохраняет новый урок.
        В случае ошибки, выбрасывает исключение PermissionDenied.
        """

        # Получаем курс из сериализатора
        course = serializer.validated_data['course']

        # Проверяем, что курс существует
        if not Course.objects.filter(id=course.id).exists():
            raise PermissionDenied("Курс не существует.")  # Выбрасываем ошибку, если курс не найден

        # Проверяем, что текущий пользователь является владельцем курса
        if course.author != self.request.user:
            raise PermissionDenied(
                "Вы можете создавать уроки только в своих курсах.")  # Выбрасываем ошибку, если пользователь не
            # владелец курса

        # Если все проверки прошли, сохраняем урок
        serializer.save()  # Сохраняем урок в базе данных


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    lookup_field = 'id'
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class LearnFlashcards(APIView):
    """Список карточек в уроке, для изучения его"""
    permission_classes = [IsAuthenticatedAndEnrolled]
    http_method_names = ["get"]

    def get(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        user = request.user

        # Передаем lesson в view для проверки разрешений
        self.check_object_permissions(request, lesson)

        # получения карточек для изучения
        learner_flashcards = FlashCard.objects.filter(
            lesson=lesson,
            learnerflashcard__user=user,
            learnerflashcard__learned_word=False
        )

        serializer = FlashCardSerializer(learner_flashcards, many=True)
        return Response(serializer.data)


class ResetResultLesson(APIView):
    """Сброс результатов урока, обнуления выученных слов в уроке"""
    permission_classes = [IsAuthenticatedAndEnrolled]
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        user = request.user

        # Передаем lesson в view для проверки разрешений
        self.check_object_permissions(request, lesson)

        # Получаем все записи LearnerFlashCard для данного урока и пользователя
        learner_flashcards = LearnerFlashCard.objects.filter(
            flashcard__lesson=lesson,
            user=user
        )

        # Обновляем поле learned_word на False
        learner_flashcards.update(learned_word=False)

        # Перенаправление на метод learn_flashcards
        return redirect('lesson-learn', pk=pk)
