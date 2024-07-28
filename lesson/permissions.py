from rest_framework import permissions


class IsAuthenticatedAndEnrolled(permissions.BasePermission):
    """Проверка что пользоватеь подписан на курс"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь аутентифицирован и что пользователь подписан на курс
        return obj.course.students.filter(id=request.user.id).exists()


class IsAuthor(permissions.BasePermission):
    """Проверям автор ли курса"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.course.author == request.user
