from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Проверям автор ли курса"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthenticatedAndEnrolled(permissions.BasePermission):
    """Проверка, что пользователь подписан на курс"""

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверяем, что  пользователь подписан на курс
        return obj.students.filter(id=request.user.id).exists()



