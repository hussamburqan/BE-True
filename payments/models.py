from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    STATUS_CHOICES = [
        ('initialized', 'Initialized'),   # تم إنشاء المعاملة على مزود الدفع
        ('processing', 'Processing'),     # قيد المعالجة
        ('requires_action', 'Requires Action'),
        ('succeeded', 'Succeeded'),       # نجحت
        ('failed', 'Failed'),             # فشلت
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]

    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider     = models.CharField(max_length=32, default='lahza')  # اسم المزود
    provider_id  = models.CharField(max_length=255, unique=True)     # transaction_id / reference من لحظة
    amount       = models.DecimalField(max_digits=10, decimal_places=2)
    currency     = models.CharField(max_length=10, default='ILS')    # العملة المحلية افتراضيًا
    status       = models.CharField(max_length=32, choices=STATUS_CHOICES)
    checkout_url = models.URLField(blank=True, null=True)            # رابط الدفع المُستضاف (إن وُجد)
    metadata     = models.JSONField(default=dict, blank=True)        # أي بيانات إضافية (طلب، عميل، …)
    created_at   = models.DateTimeField(default=timezone.now)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} – {self.amount} {self.currency} ({self.status})"
