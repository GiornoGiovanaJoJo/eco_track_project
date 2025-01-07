from rest_framework import permissions

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # здесь ты пишешь логику
        return request.user.is_authenticated and request.user.role == 'admin'


class IsEditorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'editor']


class IsAuthenticatedOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated