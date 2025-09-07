from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Participant, Enrollment, Payment
from courses.models import Course

# === Admin Serializers ===
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id','full_name','email','phone','notes','created_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    participant_id = serializers.PrimaryKeyRelatedField(
        source='participant', queryset=Participant.objects.all(), write_only=True, required=True
    )
    course_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id','participant','participant_id','course','course_title','is_active','created_at']

    def get_course_title(self, obj):
        return getattr(obj.course, 'title_en', '') or getattr(obj.course, 'title_ar', '')

class PaymentSerializer(serializers.ModelSerializer):
    enrollment_info = EnrollmentSerializer(source='enrollment', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id','enrollment','enrollment_info','method','amount','currency',
            'status','bank_reference','cash_location','note','created_at'
        ]

# === Public Create Serializer ===
class PublicEnrollmentCreateSerializer(serializers.Serializer):
    # مدخلات المستخدم العامة
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.filter(is_active=True))
    name   = serializers.CharField(max_length=120)
    email  = serializers.EmailField()
    phone  = serializers.CharField(max_length=20)
    payment_method = serializers.ChoiceField(choices=[('bank_transfer','bank_transfer'),('in_person','in_person')])
    transfer_reference = serializers.CharField(max_length=120, required=False, allow_blank=True)
    note = serializers.CharField(max_length=240, required=False, allow_blank=True)
    locale = serializers.ChoiceField(choices=[('ar','ar'),('en','en')], required=False, default='ar')

    def validate(self, attrs):
        course = attrs['course']

        # إغلاق التسجيل إذا انتهى
        reg_end = getattr(course, 'registration_end_date', None) or getattr(course, 'end_date', None)
        if reg_end:
            try:
                from datetime import date, datetime
                if isinstance(reg_end, datetime):
                    is_past = reg_end < timezone.now()
                else:
                    is_past = reg_end < date.today()
                if is_past:
                    raise serializers.ValidationError({'course': 'registration_closed'})
            except Exception:
                pass

        # منع الدفع الوجاهي لو أونلاين
        if getattr(course, 'is_online', False) and attrs['payment_method'] == 'in_person':
            raise serializers.ValidationError({'payment_method': 'in_person_not_allowed_for_online'})

        # مرجع التحويل مطلوب إذا bank_transfer
        if attrs['payment_method'] == 'bank_transfer' and not attrs.get('transfer_reference'):
            raise serializers.ValidationError({'transfer_reference': 'required_for_bank_transfer'})

        return attrs

    @transaction.atomic
    def create(self, validated):
        course: Course = validated['course']
        name   = validated['name'].strip()
        email  = validated['email'].lower().strip()
        phone  = validated['phone'].strip()
        pmethod= validated['payment_method']
        tref   = validated.get('transfer_reference','').strip()
        note   = validated.get('note','').strip()

        # 1) participant
        participant, _ = Participant.objects.get_or_create(
            email=email,
            defaults={'full_name': name, 'phone': phone}
        )
        # حدّث الاسم/الرقم لو فاضية أو تغيّرت
        if name and participant.full_name != name:
            participant.full_name = name
        if phone and participant.phone != phone:
            participant.phone = phone
        participant.save()

        # 2) enrollment
        enrollment, _ = Enrollment.objects.get_or_create(
            participant=participant, course=course,
            defaults={'is_active': True}
        )

        # 3) payment
        method_map = {'bank_transfer': Payment.METHOD_BANK, 'in_person': Payment.METHOD_CASH}
        pay = Payment(
            enrollment=enrollment,
            method=method_map[pmethod],
            note=note,
        )
        if pay.method == Payment.METHOD_BANK:
            pay.bank_reference = tref
        # amount يأخذ من سعر الدورة تلقائيًا عبر save()
        try:
            pay.save()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict or {'detail': e.messages})

        # ردّ بسيط للفرونت
        return {
            'enrollment_id': enrollment.id,
            'payment_id': pay.id,
            'status': pay.status,
            'method': pmethod,
            'amount': str(pay.amount),
            'currency': pay.currency,
        }
