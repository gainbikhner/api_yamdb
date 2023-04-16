from rest_framework import permissions


class IsNotMe(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.data.get('username') != 'me'

# class IsUnique(permissions.BasePermission()):
#     def has_permission(self, request, view):
#         return request.data.get('username') != 'me'
