from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import permissions
from jwt import decode as jwt_decode, InvalidTokenError
from django.conf import settings
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    السماح للقراءة للجميع، والكتابة فقط للمشرف.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CanUpdateStatus(permissions.BasePermission):
    """
    يسمح فقط للمستخدمين superuser بتعديل أو حذف الكورس.
    """

    def has_permission(self, request, view):
        if request.method not in ['PUT', 'PATCH', 'DELETE']:
            return True  # السماح بالقراءة لأي أحد

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied("Authentication credentials were not provided.")

        token = auth_header.split(' ')[1]

        try:
            decoded = jwt_decode(token, options={"verify_signature": False})
            if not decoded.get('is_superuser'):
                raise PermissionDenied("You do not have permission to edit/delete this course.")
        except InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        return True