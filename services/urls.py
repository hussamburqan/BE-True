from django.urls import path
from .views import (
    LatestServicesView, ServiceListCreateView, ServiceRetrieveUpdateDestroyView,
    ServiceRequestListCreateView, ServiceRequestRetrieveUpdateView
)

urlpatterns = [
    path('services', ServiceListCreateView.as_view()),
     path('services/latest', LatestServicesView.as_view()),
    path('services/<int:pk>', ServiceRetrieveUpdateDestroyView.as_view()),
    path('requests', ServiceRequestListCreateView.as_view()),
    path('requests/<int:pk>', ServiceRequestRetrieveUpdateView.as_view()),
]
