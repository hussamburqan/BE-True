from tokenize import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import *
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

MAX_PER_HOUR = 4

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    يقبل:  { "tel_number": "...", "password": "..." }
    يعيد:  { "access": "...", "refresh": "...", "name": "...", ... }
    """
    serializer_class = TelNumberTokenObtainPairSerializer


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    يحتاج Header: Authorization: Bearer <access>
    Body: {"refresh": "<refresh_token>"}
    يقوم بحظر (blacklist) الـ refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_205_RESET_CONTENT)
    
def _rate_limit_key(user_id: int, dt=None) -> str:
    dt = dt or timezone.now()
    bucket = dt.strftime("%Y%m%d%H")
    return f"pwreset:{user_id}:{bucket}"

def _seconds_until_next_hour(dt=None) -> int:
    dt = dt or timezone.now()
    next_hour = (dt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return max(5, int((next_hour - dt).total_seconds()))

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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

class VerifyResetPasswordLinkView(APIView):
    """
    GET /api/auth/reset-password/verify/?uidb64=<...>&token=<...>
    200 لو صالح، 400 لو منتهي/غير صالح
    """
    def get(self, request):
        uidb64 = request.query_params.get('uidb64')
        token  = request.query_params.get('token')
        if not uidb64 or not token:
            return Response({"code": "missing_params", "detail": "Missing uidb64 or token."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"code": "invalid_uid", "detail": "Invalid UID."},
                            status=status.HTTP_400_BAD_REQUEST)

        gen = PasswordResetTokenGenerator()
        if not gen.check_token(user, token):
            return Response({"code": "token_invalid_or_expired", "detail": "Invalid or expired token."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "OK"}, status=status.HTTP_200_OK)
    
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].strip().lower()

        generic_ok = Response({"detail": "If the email exists, a reset link will be sent."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return generic_ok

        now = timezone.now()
        key = _rate_limit_key(user.id, now)
        ttl = _seconds_until_next_hour(now)

        cache.add(key, 0, timeout=ttl)
        try:
            current = cache.incr(key)
        except Exception:
            cache.add(key, 0, timeout=ttl)
            current = cache.incr(key)

        if current > MAX_PER_HOUR:
            remaining = ttl // 60  
            return Response(
                {
                    "code": "rate_limited",
                    "detail": f"Too many password reset requests. Try again in ~{remaining} minutes."
                },
                status=429
            )

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"

        send_mail(
            subject="Password reset",
            message=f"Use this link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return generic_ok
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            uidb64 = request.data.get('uidb64')
            if not uidb64:
                return Response({"detail": "Missing UID."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (User.DoesNotExist, ValueError, TypeError):
                return Response({"detail": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)

            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
            return Response({"detail": "Password reset successful."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profile updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)