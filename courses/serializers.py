import base64
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework import serializers
from PIL import Image, UnidentifiedImageError

from .models import Course, Review


class Base64ImageField(serializers.ImageField):
    """
    يقبل:
    - 'data:image/<ext>;base64,<data>'
    - أو base64 خام بدون الهيدر (اختياري)
    ويتحقق بالصورة باستخدام Pillow ويضبط الامتداد الصحيح.
    """
    default_error_messages = {
        'invalid_image': 'البيانات المرسلة ليست صورة صالحة.',
        'decode_error': 'فشل فك ترميز base64.',
    }

    def to_internal_value(self, data):
        # لو data:image/..;base64,..
        if isinstance(data, str) and data.startswith('data:image'):
            try:
                header, img_b64 = data.split(';base64,')
            except ValueError:
                self.fail('decode_error')

            # امتداد مقترح من الهيدر (بنصح لاحقًا نستبدله بالامتداد الفعلي)
            hinted_ext = header.split('/')[-1].lower()

            # فك الترميز
            try:
                file_data = base64.b64decode(img_b64)
            except Exception:
                self.fail('decode_error')

        # base64 خام (بدون header)
        elif isinstance(data, str):
            try:
                file_data = base64.b64decode(data)
            except Exception:
                return super().to_internal_value(data)  # خلّي DRF يتصرف
            hinted_ext = 'jpg'  # افتراض مؤقت

        else:
            return super().to_internal_value(data)

        # تحقّق من أنها صورة فعلًا واستخرج الفورمات
        try:
            with Image.open(BytesIO(file_data)) as img:
                fmt = (img.format or '').lower()  # مثال: 'jpeg', 'png', 'webp'
        except UnidentifiedImageError:
            self.fail('invalid_image')

        # خريطة لتحويل الامتدادات الشائعة
        ext_map = {
            'jpeg': 'jpg',
            'jpg': 'jpg',
            'png': 'png',
            'gif': 'gif',
            'webp': 'webp',
            'bmp': 'bmp',
            'tiff': 'tiff',
        }
        final_ext = ext_map.get(fmt) or ext_map.get(hinted_ext) or 'jpg'
        file_name = f"upload.{final_ext}"

        return ContentFile(file_data, name=file_name)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer_name', 'rating', 'comment', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'is_active', 'description', 'curriculum', 'image',
            'price', 'created_at', 'updated_at', 'start_date', 'end_date'
        ]


class CourseListSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'is_active', 'description', 'curriculum', 'image',
            'price', 'created_at', 'updated_at', 'start_date', 'end_date'
        ]
