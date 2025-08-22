# payments/webhooks.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Payment

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def lahza_webhook(request):
    event = (request.data.get("event") or "").lower()
    data  = request.data.get("data", {})
    provider_id = data.get("reference") or data.get("transaction_id") or data.get("id")

    if not provider_id:
        return Response({"ok": False, "reason": "missing provider_id"}, status=400)

    try:
        payment = Payment.objects.get(provider_id=provider_id, provider='lahza')
    except Payment.DoesNotExist:
        return Response({"ok": False, "reason": "payment not found"}, status=404)

    mapping = {
        "charge.success": "succeeded",
        "payment.success": "succeeded",
        "charge.failed": "failed",
        "payment.failed": "failed",
        "refund.success": "refunded",
        "payment.cancelled": "canceled",
    }
    if event in mapping:
        payment.status = mapping[event]
        payment.save(update_fields=["status", "updated_at"])

    return Response({"ok": True})
