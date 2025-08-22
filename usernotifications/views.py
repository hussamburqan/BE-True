from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Notification
from .serializers import NotificationSerializer, MarkReadSerializer


class IsOwner(permissions.BasePermission):
    """
    يتحقق أن الكائن يخص المستخدم.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# ----------  GET /notifications ----------
class NotificationListView(generics.ListAPIView):
    serializer_class   = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class   = PageNumberPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# ----------  PUT /notifications/<id>/read ----------
class NotificationReadView(generics.UpdateAPIView):
    serializer_class   = MarkReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset           = Notification.objects.all()
    lookup_url_kwarg   = 'notif_id'

    def perform_update(self, serializer):
        serializer.save(is_read=True)


# ----------  POST /notifications/mark-all-read ----------
class NotificationMarkAllReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        updated = (
            Notification.objects
            .filter(user=request.user, is_read=False)
            .update(is_read=True)
        )
        return Response(
            {"detail": f"{updated} notifications marked as read."},
            status=status.HTTP_200_OK
        )
