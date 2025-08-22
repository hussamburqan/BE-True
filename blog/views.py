from rest_framework import generics, permissions
from .models import Post, Category
from .serializers import (
    CategorySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostSerializer,
)
from .permissions import *

# ----------  القراءة للجميع  ----------
class PostListView(generics.ListAPIView):
    queryset = Post.objects.select_related('category').all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.select_related('category')
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CanManageCategory]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CanManageCategory]

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CanManagePost]

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CanManagePost]

class CategoryPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Post.objects.filter(category__id=category_id)