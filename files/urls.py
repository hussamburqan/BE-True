from django.urls import path
from .views import (
    FileUploadView,
    BulkUploadView,
    FileRetrieveView,
    FileDeleteView,
)

urlpatterns = [
    path('files/upload',        FileUploadView.as_view(),     name='file-upload'),
    path('files/bulk-upload',   BulkUploadView.as_view(),     name='file-bulk-upload'),
    path('files/<int:file_id>', FileRetrieveView.as_view(),   name='file-retrieve'),
    path('files/<int:file_id>', FileDeleteView.as_view(),     name='file-delete'),
]
