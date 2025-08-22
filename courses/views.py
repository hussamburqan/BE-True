from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Course, Review
from .serializers import CourseSerializer, CourseListSerializer, ReviewSerializer
from .permisiions import *

class CourseCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanAddCourse]

    def get_serializer_class(self):
        return CourseSerializer if self.request.method == 'POST' else CourseListSerializer

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CanEditOrDeleteCourse,CanGetCourse]
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return []
        return [permissions.AllowAny()]

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    def get_serializer_class(self):
        return CourseListSerializer

class CurriculumView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        return Response({'curriculum': course.curriculum})


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Review.objects.filter(course_id=course_id)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs['pk']
        course = generics.get_object_or_404(Course, pk=course_id)
        if Review.objects.filter(course=course, user=self.request.user).exists():
            raise PermissionDenied("You have already reviewed this course.")
        serializer.save(user=self.request.user, course=course)
