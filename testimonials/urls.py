from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicTestimonialCreateView, AdminTestimonialViewSet

router = DefaultRouter()
router.register(r'admin/testimonials', AdminTestimonialViewSet, basename='admin-testimonials')

urlpatterns = [
    path('public/', PublicTestimonialCreateView.as_view(), name='public-testimonials-create'),
    path('', include(router.urls)),
]
