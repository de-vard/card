from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedAndEnrolled, IsAuthorOrReadOnly
from api.serializers import CourseSerializer, LessonSerializer, FlashCardSerializer
from course.models import Course
from flashcard.models import FlashCard
from lesson.models import Lesson


class CourseViewSet(viewsets.ModelViewSet):
    """Управление курсами: создание, обновление, удаления и получение списка и деталей"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedAndEnrolled]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return super().get_permissions()


class EnrollCourseView(APIView):
    """Подписка на курс"""
    authentication_classes = [BasicAuthentication]

    def post(self, request, pk, *args, **kwargs):
        course = Course.objects.get(pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})


class UnenrollCourseView(APIView):
    """Отписка с курса"""
    authentication_classes = [BasicAuthentication]

    def post(self, request, pk, *args, **kwargs):
        course = Course.objects.get(pk=pk)
        course.students.remove(request.user)
        return Response({'unenrolled': True})


class LessonViewSet(viewsets.ModelViewSet):
    """Управление уроками: создание, обновление, удаления и получение списка и деталей"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedAndEnrolled]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return super().get_permissions()


class FlashCardViewSet(viewsets.ModelViewSet):
    """Управление карточками: создание, обновление, удаления и получение списка и деталей"""
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedAndEnrolled]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return super().get_permissions()
