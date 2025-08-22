from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import permissions
from jwt import decode as jwt_decode, InvalidTokenError
from django.conf import settings
class CanAddCourse(permissions.BasePermission):
    """
    يسمح فقط للمستخدم الذي يحمل توكن يحتوي على is_superuser=True بإضافة كورسات.
    """

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied("Authentication credentials were not provided.")

        token = auth_header.split(' ')[1]

        try:
            # فك التوكن (لا تتحقق من التوقيع هنا فقط تفكيره لقراءة محتواه)
            decoded = jwt_decode(token, options={"verify_signature": False})
            print(decoded)
            if not decoded.get('is_superuser'):
                raise PermissionDenied("You do not have permission to add courses.")
        except InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        return True

class CanEditOrDeleteCourse(permissions.BasePermission):
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

class CanGetCourse(permissions.BasePermission):
    """
    يسمح فقط للمستخدمين superuser بتعديل أو حذف الكورس.
    """

    def has_permission(self, request, view):
        

        return True