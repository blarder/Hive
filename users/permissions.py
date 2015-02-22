__author__ = 'brettlarder'
from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):

    def has_permission(self, request, view):
        return request.user.verified


class DebugAllowAll(BasePermission):

    def has_permission(self, request, view):
        return True
