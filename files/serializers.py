from rest_framework import serializers
from .models import UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UploadedFile
        fields = ['id', 'file', 'original_name', 'size', 'content_type', 'uploaded_at']
        read_only_fields = ['id', 'original_name', 'size', 'content_type', 'uploaded_at']

    def create(self, validated_data):
        request_file = self.context['request'].FILES['file']
        return UploadedFile.objects.create(
            file=request_file,
            original_name=request_file.name,
            size=request_file.size,
            content_type=request_file.content_type or '',
            uploaded_by=self.context['request'].user if self.context['request'].user.is_authenticated else None,
        )


class BulkUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False
    )

    def create(self, validated_data):
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        objs = []
        for f in validated_data['files']:
            objs.append(UploadedFile(
                file=f,
                original_name=f.name,
                size=f.size,
                content_type=f.content_type or '',
                uploaded_by=user,
            ))
        return UploadedFile.objects.bulk_create(objs)
