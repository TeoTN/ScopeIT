from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsObjectOwnerOrAdmin(BasePermission):
    """
    This permission is used to grant access only to a user which is in staff group or is owner of given object.
    Method has_permission is superior to the has_object_permission.
    Method has_permission will deny access to non-administrative account accessing to the list of users.
    Method has_object_permission will grant access to user trying to view his/her own profile or to admin.
    """
    def has_permission(self, request, view):
        return view.action == 'retrieve' or \
               request.user.is_staff or \
               request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user == obj or \
               request.user.is_staff or \
               request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    """
    This permission will grant access only to safe methods (e.g. GET) unless request comes from admin
    """
    def has_permission(self, request, view):
        return request.user.is_staff or \
               request.user.is_superuser or \
               request.method in SAFE_METHODS


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    This permission will grant access to list when:
    1. Request user is admin
    2. Requested method is in SAFE_METHODS
    3. User is owner of updated data
    """
    def has_permission(self, request, view):
        return view.action == 'retrieve'


    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or \
               request.user.is_superuser or \
               request.method in SAFE_METHODS or \
               request.user == obj


class UserPermissionScheme(BasePermission):
    def has_permission(self, request, view):
        return (view.action != 'list' and \
                view.action != 'create') or \
               request.user.is_staff or \
               request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user == obj or \
               request.user.is_staff or \
               request.user.is_superuser