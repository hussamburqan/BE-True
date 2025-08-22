from rest_framework import generics, permissions

from portfolio.permissions import CanAddProject,AnyUser, CanDeleteProject, CanUpdateProject
from .models import PortfolioItem
from .serializers import PortfolioSerializer

class PortfolioListView(generics.ListAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.AllowAny]

class PortfoliolatestListView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [AnyUser]
    pagination_class = None
    def get_queryset(self):
        return PortfolioItem.objects.all()[:3]

class PortfolioDetailView(generics.RetrieveAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.AllowAny]

class PortfolioCreateView(generics.CreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [CanAddProject]

class PortfolioUpdateView(generics.UpdateAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [CanUpdateProject]
    lookup_url_kwarg = 'item_id'

class PortfolioDeleteView(generics.DestroyAPIView):
    queryset = PortfolioItem.objects.all()
    permission_classes = [CanDeleteProject]
    lookup_url_kwarg = 'item_id'
