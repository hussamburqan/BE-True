from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from jwt import decode as jwt_decode, InvalidTokenError

def decode_token(request):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        raise PermissionDenied("Authentication required.")
    token = auth.split(" ")[1]
    try:
        return jwt_decode(token, options={"verify_signature": False})
    except InvalidTokenError:
        raise PermissionDenied("Invalid token.")

class CanMessage(permissions.BasePermission):
    """
    يسمح فقط للمستخدم superuser بإضافة/تعديل/حذف التصنيفات.
    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        decoded = decode_token(request)
        return decoded.get("is_superuser", False)