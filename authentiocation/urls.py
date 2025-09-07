from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView, LogoutView, RegisterView,
    ChangePasswordView, ProfileView,
)

urlpatterns = [

    path('public/login/',   LoginView.as_view(),          name='public-auth-login'),
    path('public/refresh/', TokenRefreshView.as_view(),   name='public-auth-refresh'),

    path('me/',                 ProfileView.as_view(),        name='auth-profile'),
    path('me/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),
    path('me/logout/',          LogoutView.as_view(),         name='auth-logout'),

    path('admin/users/create/', RegisterView.as_view(),       name='admin-users-create'),
]
