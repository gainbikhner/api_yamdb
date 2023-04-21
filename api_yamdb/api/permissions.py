from rest_framework import permissions


class IsAdmin(permissions.IsAuthenticatedOrReadOnly):
    """Проверка доступа: администратор."""
    message = 'Доступно только администратору.'

    def has_permission(self, request, view):
        if str(request.user) != 'AnonymousUser':
            return request.user.role == 'admin' or request.user.is_superuser


class IsModerator(permissions.IsAuthenticatedOrReadOnly):
    """Проверка доступа: модератор."""
    message = 'Доступно модератору.'

    def has_permission(self, request, view):
        return request.user.role == 'moderator' or IsAdmin()
