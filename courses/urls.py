from django.urls import path
from .views import *

urlpatterns = [
    path('courses', CourseListView.as_view(), name='course-list-create'),
    path('courses', CourseCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/curriculum', CurriculumView.as_view(), name='course-curriculum'),
    path('courses/<int:pk>/reviews', ReviewListView.as_view(), name='course-reviews'),
    path('courses/<int:pk>/reviews/add', ReviewCreateView.as_view(), name='course-review-add'),
]
