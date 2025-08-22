from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login',  LoginView.as_view(),  name='jwt-login'),
    path('refresh', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('logout', LogoutView.as_view(), name='jwt-logout'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('reset-password/verify', VerifyResetPasswordLinkView.as_view()),
    path('change-password', ChangePasswordView.as_view()),

]
