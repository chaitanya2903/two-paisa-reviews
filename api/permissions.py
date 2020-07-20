from rest_framework import permissions
from rest_framework.authentication import *

class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [
                            BasicAuthentication,
                            SessionAuthentication
                        ]
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == 'GET':
            return True
        if user and user.is_authenticated:
            return user.is_superuser
        return False

    def has_permission(self, request, view):
        user = request.user
        if request.method == 'GET':
            return True
        if user and user.is_authenticated:
            return user.is_superuser
        return False



class UserUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return obj.id == request.user.id

class ReviewPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == 'GET':
            return True
        else:
            return obj.reviewer.id == request.user.id
        return False
