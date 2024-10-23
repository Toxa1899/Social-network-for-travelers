from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class BlockCreatePosts(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, "create_posts", False)


class IsNotAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_superuser


class IsNotBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:

            return getattr(request.user, "is_blocked", True)
        return True
