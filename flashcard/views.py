from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from rest_framework.views import APIView

from course.models import Course
from flashcard.permissions import IsAuthenticatedAndEnrolled, IsAuthor

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashcard.permissions import IsAuthenticatedAndEnrolled
from flashcard.serializers import FlashCardSerializer

from flashcard.models import FlashCard, LearnerFlashCard
from lesson.models import Lesson


class FlashCardListAPIView(generics.ListAPIView):
    """Список карточки"""
    http_method_names = ["get"]
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FlashCardSerializer


class FlashCardRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотер карточки без редактирования"""
    http_method_names = ["get"]
    lookup_field = "id"
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FlashCardSerializer


class FlashCardRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование карточки"""
    lookup_field = 'id'
    http_method_names = ["put"]
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = FlashCardSerializer


class FlashCardCreateAPIView(generics.CreateAPIView):
    """Создание карточки"""
    http_method_names = ["post"]
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthor, IsAuthenticated]
    serializer_class = FlashCardSerializer

    def perform_create(self, serializer):
        """
        Этот метод вызывается при создании новой флешкарточки. Он выполняет проверки:
        1. Проверяет, что урок существует.
        2. Проверяет, что текущий пользователь является владельцем курса, к которому относится урок.

        Если проверки прошли успешно, сохраняет новую карточку.
        В случае ошибки выбрасывает исключение PermissionDenied.
        """
        # Получаем урок из сериализатора
        lesson = serializer.validated_data['lesson']

        # Проверяем, что урок существует
        if not Lesson.objects.filter(id=lesson.id).exists():
            raise PermissionDenied("Урок не существует.")  # Ошибка, если урок не найден

        # Проверяем, что текущий пользователь является владельцем курса, которому принадлежит урок
        if lesson.course.author != self.request.user:
            raise PermissionDenied(
                "Вы можете создавать карточки только в своих уроках."
            )  # Ошибка, если пользователь не владелец курса

        # Если все проверки пройдены, сохраняем карточку
        serializer.save()


class FlashCardDestroyAPIView(generics.DestroyAPIView):
    """Удаление карточки"""
    lookup_field = 'id'
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class KnowFlashCard(APIView):
    """Знает пользователь карточку"""
    http_method_names = ["post"]
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        """Отметить слово как известное"""
        flashcard = get_object_or_404(FlashCard, pk=pk)

        # Передаем lesson в view для проверки разрешений
        self.check_object_permissions(request, flashcard)

        learner_flashcard, _ = LearnerFlashCard.objects.get_or_create(user=request.user, flashcard=flashcard)
        learner_flashcard.learned_word = True
        learner_flashcard.save()
        return Response({'status': 'marked as known'}, status=status.HTTP_200_OK)


class UnknownFlashCard(APIView):
    """Не знает пользователь карточку"""
    http_method_names = ["post"]
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        """Отметить слово как неизвестное"""
        flashcard = get_object_or_404(FlashCard, pk=pk)

        # Передаем lesson в view для проверки разрешений
        self.check_object_permissions(request, flashcard)

        learner_flashcard, _ = LearnerFlashCard.objects.get_or_create(user=request.user, flashcard=flashcard)
        learner_flashcard.learned_word = False
        learner_flashcard.save()
        return Response({'status': 'marked as unknown'}, status=status.HTTP_200_OK)
