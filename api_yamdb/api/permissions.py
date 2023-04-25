from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка доступа: администратор."""
    message = 'Доступно только администратору.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)


class IsAdminOrSafeMethods(IsAdmin):
    """Проверка доступа: администратор."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or super().has_permission(request, view)


class IsAuthor(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        is_safe_method = request.method in permissions.SAFE_METHODS
        is_author = obj.author == request.user
        return is_safe_method or is_author or request.user.role == 'moderator' or request.user.role == 'admin' or request.user.is_superuser


class IsModerator(IsAdminOrSafeMethods):
    """Проверка доступа: модератор."""
    message = 'Доступно модератору.'

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or super().has_permission(request, view)
