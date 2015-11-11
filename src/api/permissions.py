from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS


class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.user.username


class IsPostRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class IsRequestUser(BasePermission):
    """
    Check if data sent to API contain user equal to request user
    """
    def has_permission(self, request, view):
        return request.data.get('user', None) == request.user.username


class UserProfilePermission(BasePermission):
    """
    Authentication scheme:
        GET     -> admin or action is retrieve
        POST    -> request user or admin
        PUT     -> admin or owner
        DELETE  -> request user or admin
        PATCH   -> owner or admin
    """
    def has_permission(self, request, view):
        is_admin = request.user.is_staff or request.user.is_superuser
        if is_admin:
            return True
        if request.method in SAFE_METHODS:
            return view.action == 'retrieve'
        if request.method == 'POST':
            is_post = IsPostRequest().has_permission(request, view)
            is_req_user = IsRequestUser().has_permission(request, view)
            return (is_req_user and is_post)
        return True  # Continue to has_object_permission

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_staff or request.user.is_superuser
        is_owner = IsObjectOwner().has_object_permission(request, view, obj)
        return is_admin or is_owner
