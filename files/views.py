from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from .models import UploadedFile
from .serializers import FileUploadSerializer, BulkUploadSerializer


class FileUploadView(generics.CreateAPIView):
    serializer_class    = FileUploadSerializer
    permission_classes  = [permissions.IsAuthenticated]
    parser_classes      = [  # لدعم multipart
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ]


class BulkUploadView(generics.GenericAPIView):
    serializer_class   = BulkUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = FileUploadView.parser_classes

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'files': request.FILES.getlist('files')})
        serializer.is_valid(raise_exception=True)
        created_objs = serializer.save()
        data = FileUploadSerializer(created_objs, many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_201_CREATED)


class FileRetrieveView(generics.GenericAPIView):
    """
    GET يعيد الملف نفسه إذا لم يُرسل Query param ?meta=1.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, file_id):
        obj = get_object_or_404(UploadedFile, id=file_id)
        if request.query_params.get('meta'):
            data = FileUploadSerializer(obj, context={'request': request}).data
            return Response(data)
        try:
            return FileResponse(obj.file.open('rb'), as_attachment=True, filename=obj.original_name)
        except FileNotFoundError:
            raise Http404("File not found on disk")


class FileDeleteView(generics.DestroyAPIView):
    queryset           = UploadedFile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    lookup_url_kwarg   = 'file_id'

    def perform_destroy(self, instance):
        # optional: verify ownership
        if instance.uploaded_by and instance.uploaded_by != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("Not allowed")
        instance.file.delete(save=False)  # حذف من القرص
        instance.delete()
