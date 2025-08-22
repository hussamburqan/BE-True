from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework import permissions
from jwt import decode as jwt_decode, InvalidTokenError
from django.conf import settings
class AnyUser(permissions.BasePermission):
    def has_permission(self, request, view):
       
        return True