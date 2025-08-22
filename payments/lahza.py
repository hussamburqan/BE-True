# payments/lahza.py
import requests
from django.conf import settings

class LahzaError(Exception):
    pass

def _headers():
    return {
        "Authorization": f"Bearer {settings.LAHZA_SECRET_KEY}",
        "Content-Type": "application/json",
    }

def initialize_payment(*, amount, currency="ILS", email=None, description=None, metadata=None, callback_url=None):
    url = f"{settings.LAHZA_API_BASE}/transaction/initialize"
    payload = {
        "amount": int(round(float(amount) * 100)),  # بالمليم/السنت
        "currency": currency,
        "email": email,
        "description": description,
        "metadata": metadata or {},
        "callback_url": callback_url or getattr(settings, "LAHZA_CALLBACK_URL", None),
    }

    r = requests.post(url, json=payload, headers=_headers(), timeout=30)
    if r.status_code >= 400:
        raise LahzaError(f"Initialize failed: {r.status_code} {r.text}")

    outer = r.json()
    inner = outer.get("data") or {}

    provider_id  = inner.get("reference")
    checkout_url = inner.get("authorization_url") or inner.get("payment_url")

    if not provider_id:
        # نطبع الرد كامل للمساعدة في الديباج
        raise LahzaError(f"Missing provider_id in response: {outer}")

    return {
        "provider_id": provider_id,
        "checkout_url": checkout_url,
        "raw": outer,
    }

def verify_payment(provider_id: str):
    # حسب توثيق لحظة: verify بالـ reference
    url = f"{settings.LAHZA_API_BASE}/transaction/verify/{provider_id}"
    r = requests.get(url, headers=_headers(), timeout=30)
    if r.status_code >= 400:
        raise LahzaError(f"Verify failed: {r.status_code} {r.text}")

    outer = r.json()
    inner = outer.get("data") or {}

    # بعض الأنظمة ترجع status داخل data أو أعلى
    lahza_status = (inner.get("status") or outer.get("status") or "").lower()

    # تطبيع الحالات
    normalized_status = {
        "success": "succeeded",
        "successful": "succeeded",
        "paid": "succeeded",
        "succeeded": "succeeded",
        "pending": "processing",
        "processing": "processing",
        "failed": "failed",
        "cancelled": "canceled",
        "canceled": "canceled",
        "refunded": "refunded",
        True: "succeeded",   # بعض الـ APIs ترجع boolean
        False: "failed",
    }.get(lahza_status, "processing")

    amount_minor = inner.get("amount")  # غالبًا بالسنت
    currency     = inner.get("currency") or "ILS"

    return {
        "status": normalized_status,
        "currency": currency,
        "amount_minor": amount_minor,
        "raw": outer,
    }

def refund_payment(provider_id: str, amount_minor: int | None = None):
    url = f"{settings.LAHZA_API_BASE}/transaction/refund"
    payload = {"reference": provider_id}
    if amount_minor is not None:
        payload["amount"] = amount_minor

    r = requests.post(url, json=payload, headers=_headers(), timeout=30)
    if r.status_code >= 400:
        raise LahzaError(f"Refund failed: {r.status_code} {r.text}")
    return r.json()
