"""
API utilities for authentication and permissions
"""
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class IsFarmer(permissions.BasePermission):
    """Permission to check if user is a farmer"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'


class IsBuyer(permissions.BasePermission):
    """Permission to check if user is a buyer"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'buyer'


class IsEnterprise(permissions.BasePermission):
    """Permission to check if user is an enterprise"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'enterprise'


class IsAdmin(permissions.BasePermission):
    """Permission to check if user is an admin"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to allow users to edit only their own objects"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff
