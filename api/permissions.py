from rest_framework.permissions import BasePermission, SAFE_METHODS

def user_in_group(user, group_name):
    if not user or not user.is_authenticated:
        return False
    if hasattr(user, '_group_cache'):
        return group_name in user._group_cache
    user._group_cache = set(user.groups.values_list('name', flat=True))
    return group_name in user._group_cache

class IsLibrarianGroupOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return user_in_group(user, "Librarian")

class IsLibrarianGroupOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user_in_group(user, "Librarian")

class IsMemberGroupOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user_in_group(user, "Member")

class IsLibrarianOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return user_in_group(user, "Librarian")
