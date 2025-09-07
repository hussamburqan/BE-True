from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicTeamListView, AdminTeamViewSet

router = DefaultRouter()
router.register(r'admin/teams', AdminTeamViewSet, basename='admin-teams')

urlpatterns = [
    path('public/', PublicTeamListView.as_view(), name='public-teams-list'),
    path('', include(router.urls)),
]
