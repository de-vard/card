from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from course.permissions import IsAuthenticatedAndEnrolled, IsAuthor
from course.serializers import CourseSerializerDetails, CourseSerializerList
from course.models import Course, RegisteredUsers


# Todo: проверь код на разрешения, создай тесты для тестирования кода
class CourseListAPIView(generics.ListAPIView):
    """Список курсов"""
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializerList


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """Детальный просмотер курсов без редактирования"""
    lookup_field = "id"
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticatedAndEnrolled]
    serializer_class = CourseSerializerDetails


class CourseRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Редактирование курса"""
    lookup_field = 'id'
    queryset = Course.objects.all()
    permission_classes = [IsAuthor]
    serializer_class = CourseSerializerDetails


class CourseCreateAPIView(generics.CreateAPIView):
    """Создание курса"""
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializerDetails


class CourseDestroyAPIView(generics.DestroyAPIView):
    """Удаление курса"""
    lookup_field = 'id'
    queryset = Course.objects.all()
    permission_classes = [IsAuthor]


class EnrollCourse(APIView):
    """Подписка на курс"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        if course.students.filter(id=request.user.id).exists():
            return Response({'detail': 'Вы уже подписаны на этот курс.'}, status=status.HTTP_400_BAD_REQUEST)
        course.students.add(request.user)
        return Response({'enrolled': True})


class UnenrollCourse(APIView):
    """Отписка от курса"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        if not course.students.filter(id=request.user.id).exists():
            return Response({'detail': 'Вы не подписаны на этот курс.'}, status=status.HTTP_400_BAD_REQUEST)
        course.students.remove(request.user)
        return Response({'unenrolled': True})


class LikeCourse(APIView):
    """Лайк курса"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        registered_user, created = RegisteredUsers.objects.get_or_create(course=course, user=request.user)
        registered_user.liked = True
        registered_user.disliked = False
        registered_user.save()
        return Response({'liked': True})


class DislikeCourse(APIView):
    """Дизлайк курса"""
    permission_classes = [IsAuthenticatedAndEnrolled]

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        registered_user, created = RegisteredUsers.objects.get_or_create(course=course, user=request.user)
        registered_user.liked = False
        registered_user.disliked = True
        registered_user.save()
        return Response({'disliked': True})
