from rest_framework import permissions
from applications.account.models import BlockedUser


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class BlockCreatePosts(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            blocked_user = BlockedUser.objects.filter(
                user=request.user
            ).first()
            if blocked_user and not blocked_user.can_create_posts:
                return False
        return True


class IsNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            blocked_user = BlockedUser.objects.filter(
                user=request.user
            ).first()
            if blocked_user and blocked_user.is_blocked:
                return False
        return True


class IsNotAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_superuser
