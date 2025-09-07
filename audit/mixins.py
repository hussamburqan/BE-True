# audit/mixins.py
from __future__ import annotations

from django.db import transaction
from django.forms.models import model_to_dict
from django.utils.timezone import now

from .models import AuditLog


# حقول لا نحتفظ بها داخل اللوج
SENSITIVE_FIELDS = {"password", "token", "secret", "api_key", "apiToken"}


def _client_ip(request) -> str:
    """
    يرجّع IP الحقيقي إن وُجد (يدعم X-Forwarded-For)، وإلا Remote-Addr.
    """
    if not request:
        return ""
    xff = (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")[0].strip()
    return xff or request.META.get("REMOTE_ADDR", "") or ""


def _compact(instance, only_fields=None) -> dict:
    """
    يحوّل كائن الموديل لديكشنري صغير:
    - يلتقط الحقول الـ concrete فقط (بدون علاقات/ManyToMany)
    - يستثني الحقول الحسّاسة
    - يمكن تقليصه عبر only_fields لتوفير المساحة
    """
    fields = []
    for f in instance._meta.get_fields():
        if getattr(f, "concrete", False) and not f.many_to_many and not f.is_relation:
            if f.name not in SENSITIVE_FIELDS:
                fields.append(f.name)
    if only_fields:
        keep = set(only_fields)
        fields = [f for f in fields if f in keep]
    return model_to_dict(instance, fields=fields)


class AuditCreateOnlyMixin:
    """
    مِكسِن يسجّل عمليات (الإضافة فقط) لأي View/ViewSet.
    الاستخدام:
        class AdminXViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
            audit_fields = ["id", "title", "is_active"]  # اختياري لتقليل حجم اللوج

        class PublicCreateView(AuditCreateOnlyMixin, generics.CreateAPIView):
            audit_public_creates = True  # سجّل أيضًا إضافات الجمهور (AllowAny)

    الخصائص:
      - audit_fields:   قائمة بأسماء الحقول التي نريد حفظها داخل اللوج (اختياري).
      - audit_public_creates: لو True يسجّل إضافات الزوار/المجهولين أيضًا.
                               لو False (الافتراضي) يسجّل فقط لو المستخدم staff/superuser.
    """
    audit_fields: list[str] | None = None
    audit_public_creates: bool = False

    def _log_create(self, instance) -> None:
        request = getattr(self, "request", None)
        user = getattr(request, "user", None)

        # افتراضيًا: نسجّل فقط إضافات staff/superuser
        if not self.audit_public_creates:
            if not (user and user.is_authenticated and (user.is_staff or user.is_superuser)):
                return

        after = _compact(instance, self.audit_fields)

        def _create_log():
            AuditLog.objects.create(
                actor=user if (user and user.is_authenticated) else None,
                action=AuditLog.ACTION_CREATE,
                app_label=instance._meta.app_label,
                model=type(instance).__name__,
                object_pk=str(getattr(instance, "pk", "")),
                object_repr=str(instance)[:255],
                route=(request.path if request else "")[:255],
                method=(request.method if request else "")[:8],
                ip_address=_client_ip(request),
                user_agent=(request.META.get("HTTP_USER_AGENT", "") if request else "")[:1024],
                changes=None,                # نحتفظ بالحالة بعد الإنشاء فقط
                extra={"after": after},      # الحالة النهائية بعد الحفظ
                created_at=now(),            # اختياري؛ لدينا auto_now_add أيضاً
            )

        # نسجّل بعد نجاح الترانزاكشن
        transaction.on_commit(_create_log)

    # هوك على create فقط
    def perform_create(self, serializer):
        obj = serializer.save()
        self._log_create(obj)
        return obj
