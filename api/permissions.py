from rest_framework import permissions

from course.models import Course
from flashcard.models import FlashCard
from lesson.models import Lesson


class IsAuthenticatedAndEnrolled(permissions.BasePermission):
    """Проверка что пользоватеь подписан на курс"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь аутентифицирован и что пользователь подписан на курс

        if isinstance(obj, Course):
            return obj.students.filter(id=request.user.id).exists()
        elif isinstance(obj, Lesson):
            return obj.course.students.filter(id=request.user.id).exists()
        elif isinstance(obj, FlashCard):
            return obj.lesson.course.students.filter(id=request.user.id).exists()

        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверям автор ли курса"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # если метод безопасны(чтение)
            return True
        if isinstance(obj, Course):
            return obj.author == request.user
        elif isinstance(obj, Lesson):
            return obj.course.author == request.user
        elif isinstance(obj, FlashCard):
            return obj.lesson.course.author == request.user


