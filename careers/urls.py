from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicJoinTeamView,
    PublicInternshipApplyView,
    AdminTalentApplicationViewSet,
    AdminInternshipApplicationViewSet
)

router = DefaultRouter()
router.register(r'admin/talent-applications', AdminTalentApplicationViewSet, basename='admin-talent-apps')
router.register(r'admin/internship-applications', AdminInternshipApplicationViewSet, basename='admin-intern-apps')

urlpatterns = [

    path('public/join-team/', PublicJoinTeamView.as_view(), name='public-join-team'),
    path('public/internship-apply/', PublicInternshipApplyView.as_view(), name='public-internship-apply'),

    path('', include(router.urls)),
]
