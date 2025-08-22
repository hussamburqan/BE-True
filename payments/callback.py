# payments/callback.py
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Payment
from . import lahza

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def lahza_callback(request):
    # لحظة عادة ترجع reference كـ ?trxref=<...>&reference=<...>
    provider_id = (
        request.GET.get("reference")
        or request.GET.get("trxref")
        or request.data.get("reference")
        or request.data.get("trxref")
    )
    if not provider_id:
        return Response({"error": "missing reference/trxref"}, status=400)

    try:
        payment = Payment.objects.get(provider_id=provider_id, provider="lahza")
    except Payment.DoesNotExist:
        return Response({"error": "payment not found"}, status=404)

    # تحقّق من حالة العملية
    v = lahza.verify_payment(provider_id)
    payment.status = v["status"]
    payment.save(update_fields=["status", "updated_at"])

    # رجّع المستخدم لواجهة النتيجة في الفرونت
    front = getattr(settings, "FRONTEND_URL", "")
    return redirect(f"{front}/payment-result?status={payment.status}&ref={provider_id}")
