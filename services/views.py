from rest_framework import generics

from services.permissions import AnyUser
from .models import Service, ServiceRequest
from .serializers import ServiceSerializer, ServiceRequestSerializer

# --- Service Endpoints ---
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# --- ServiceRequest Endpoints ---
class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class LatestServicesView(generics.ListAPIView):
    """
    API لإرجاع أحدث 6 خدمات فقط.
    """
    serializer_class = ServiceSerializer
    pagination_class = None
    permission_classes = [AnyUser]
    def get_queryset(self):
        return Service.objects.order_by('-created_at')[:6]