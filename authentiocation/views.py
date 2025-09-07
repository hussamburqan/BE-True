from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from audit.mixins import AuditCreateOnlyMixin
from .serializers import (
    RegisterSerializer, EmailOrTelTokenObtainPairSerializer, ProfileSerializer
)
from true.permissions import IsStaffOrSuperuser

User = get_user_model()

class RegisterView(AuditCreateOnlyMixin, APIView): 
    """
    إنشاء مستخدم ستاف فقط (عن طريق الأدمن/الستاف).
    يمنع تمرير is_superuser هنا.
    يُسجّل عملية الإضافة فقط في جدول اللوج.
    """
    permission_classes = [IsStaffOrSuperuser]

    audit_fields = ["id", "name", "email", "tel_number", "is_staff", "is_superuser", "date_joined"]

    def post(self, request):
        data = request.data.copy()
        data['is_staff'] = True
        data.pop('is_superuser', None)

        s = RegisterSerializer(data=data, context={'request': request})
        s.is_valid(raise_exception=True)
        user = s.save()

        self._log_create(user)

        return Response({"message": "Staff user created successfully."}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    POST /auth/public/login/
    يقبل email أو tel_number أو identifier.
    يرجّع access/refresh ومعلومات مختصرة عن المستخدم.
    """
    serializer_class = EmailOrTelTokenObtainPairSerializer


class LogoutView(APIView):
    """
    POST /auth/me/logout/
    Header: Authorization: Bearer <access>
    Body:   { "refresh": "<refresh_token>" }
    يحظر (blacklist) الـ refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(APIView):
    """
    POST /auth/me/change-password/
    Body: { "old_password": "...", "new_password": "..." }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"code": "missing_params", "detail": "old_password and new_password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        if not user.check_password(old_password):
            return Response(
                {"code": "wrong_old_password", "detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    GET /auth/me/   → بيانات البروفايل
    PUT /auth/me/   → تحديث جزئي لبيانات البروفايل
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    def put(self, request):
        s = ProfileSerializer(request.user, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"detail": "Profile updated successfully."})
