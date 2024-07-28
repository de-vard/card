from rest_framework.generics import get_object_or_404

from rest_framework.views import APIView

from flashcard.permissions import IsAuthenticatedAndEnrolled, IsAuthor

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from flashcard.permissions import IsAuthenticatedAndEnrolled
from flashcard.serializers import FlashCardSerializer

from flashcard.models import FlashCard, LearnerFlashCard


class FlashCardListAPIView(generics.ListAPIView):
    """Список карточки"""
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FlashCardSerializer


class FlashCardRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотер карточки без редактирования"""
    lookup_field = "id"
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticatedAndEnrolled]
    serializer_class = FlashCardSerializer


class FlashCardRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование карточки"""
    lookup_field = 'id'
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = FlashCardSerializer


class FlashCardCreateAPIView(generics.CreateAPIView):
    """Создание карточки"""
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FlashCardSerializer


class FlashCardDestroyAPIView(generics.DestroyAPIView):
    """Удаление карточки"""
    lookup_field = 'id'
    queryset = FlashCard.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]


class KnowFlashCard(APIView):
    """Знает пользователь карточку"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        """Отметить слово как известное"""
        flashcard = get_object_or_404(FlashCard, pk=pk)
        learner_flashcard, created = LearnerFlashCard.objects.get_or_create(user=request.user, flashcard=flashcard)
        learner_flashcard.learned_word = True
        learner_flashcard.save()
        return Response({'status': 'marked as known'}, status=status.HTTP_200_OK)


class UnknownFlashCard(APIView):
    """Не знает пользователь карточку"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        """Отметить слово как неизвестное"""
        flashcard = get_object_or_404(FlashCard, pk=pk)
        learner_flashcard, created = LearnerFlashCard.objects.get_or_create(user=request.user, flashcard=flashcard)
        learner_flashcard.learned_word = False
        learner_flashcard.save()
        return Response({'status': 'marked as unknown'}, status=status.HTTP_200_OK)
