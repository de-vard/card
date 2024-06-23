from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsEnrolled
from api.serializers import CourseSerializer
from course.models import Course


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        """Подписаться на курс"""
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def unenroll(self, request, *args, **kwargs):
        """Отписаться с курса"""
        course = self.get_object()
        course.students.remove(request.user)
        return Response({'unenrolled': True})

    @action(
        detail=True, methods=['get'], serializer_class=CourseSerializer,
        authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        """Просмотр содержимого курса"""
        course = self.get_object()
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)
