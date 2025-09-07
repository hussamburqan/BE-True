from rest_framework import generics, viewsets, permissions, filters
from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import Post
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostWriteSerializer
)

class PostPublicListView(generics.ListAPIView):
    queryset = Post.objects.filter(is_published=True).order_by('-id')
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

class PostPublicDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]

class AdminPostViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    يسجّل عمليات الإضافة فقط (create) عبر AuditCreateOnlyMixin
    صلاحيات الأدمن: ستاف/سوبر فقط
    """
    queryset = Post.objects.all().order_by('-id')
    permission_classes = [IsStaffOrSuperuser]

    audit_fields = ["id", "title", "is_published", "created_at"]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['id', 'title']
    ordering_fields = ['id', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
