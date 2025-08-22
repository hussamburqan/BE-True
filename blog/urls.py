from django.urls import path
from .views import (
    CategoryPostsView, PostListView, PostDetailView,
    PostRetrieveUpdateDestroyView,PostListCreateView,
    CategoryListView,CategoryRetrieveUpdateDestroyView,CategoryListCreateView
)

urlpatterns = [
    # Category endpoints
    path('categories', CategoryListCreateView.as_view()),
    path('categories/<int:pk>', CategoryRetrieveUpdateDestroyView.as_view()),
    path('category-posts/<int:pk>',CategoryPostsView.as_view()),
    # Post endpoints
    path('posts', PostListCreateView.as_view()),
    path('posts/<int:pk>', PostRetrieveUpdateDestroyView.as_view()),
]
