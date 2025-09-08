# testimonials/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicTestimonialView, AdminTestimonialViewSet

router = DefaultRouter()
router.register(r'admin/testimonials', AdminTestimonialViewSet, basename='admin-testimonials')

urlpatterns = [
    path('public/', PublicTestimonialView.as_view(), name='public-testimonials'),  # << كان CreateAPIView
    path('', include(router.urls)),
]
