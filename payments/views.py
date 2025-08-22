from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Payment
from .serializers import (
    PaymentCreateSerializer,
    PaymentVerifySerializer,
    PaymentHistorySerializer,
    RefundSerializer,
)
from . import lahza  # from payments.lahza import ...


# ---------- إنشاء معاملة (Initialize) ----------
class PaymentCreateView(generics.GenericAPIView):
    serializer_class   = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        amount      = ser.validated_data['amount']
        currency    = ser.validated_data['currency']
        email       = ser.validated_data.get('email')
        description = ser.validated_data.get('description')

        # ميتاداتا اختيارية (مثال)
        metadata = {"user_id": request.user.id}

        try:
            init_res = lahza.initialize_payment(
                amount=amount,
                currency=currency,
                email=email,
                description=description,
                metadata=metadata,
                callback_url=settings.LAHZA_CALLBACK_URL,
            )
        except lahza.LahzaError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # خزّن السجل
        payment = Payment.objects.create(
            user=request.user,
            provider='lahza',
            provider_id=init_res["provider_id"],
            amount=amount,
            currency=currency,
            status='initialized',
            checkout_url=init_res.get("checkout_url"),
            metadata=metadata,
        )

        return Response({
            "payment_id": payment.id,
            "provider_id": payment.provider_id,
            "status": payment.status,
            "checkout_url": payment.checkout_url,  # لو موجود؛ وجّه فرونت إند عليه
        }, status=status.HTTP_201_CREATED)


# ---------- التحقق بعد العودة (Verify) ----------
class PaymentVerifyView(generics.GenericAPIView):
    serializer_class   = PaymentVerifySerializer
    permission_classes = [permissions.AllowAny]  # إن كنت تستقبله كـ callback عام

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        provider_id = ser.validated_data['provider_id']

        # جيب السجل
        try:
            payment = Payment.objects.get(provider_id=provider_id, provider='lahza')
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            verify = lahza.verify_payment(provider_id)
        except lahza.LahzaError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = verify["status"]
        payment.currency = verify.get("currency", payment.currency)
        payment.save(update_fields=['status', 'currency', 'updated_at'])

        return Response({"status": payment.status})


# ---------- التاريخ ----------
class PaymentHistoryView(generics.ListAPIView):
    serializer_class   = PaymentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


# ---------- الاسترداد (Refund) ----------
class PaymentRefundView(generics.GenericAPIView):
    serializer_class   = RefundSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        payment_id = ser.validated_data['payment_id']
        amount     = ser.validated_data.get('amount')

        payment = generics.get_object_or_404(Payment, id=payment_id)
        if payment.provider != 'lahza':
            return Response({"error": "Unsupported provider"}, status=status.HTTP_400_BAD_REQUEST)

        amount_minor = int(amount * 100) if amount else None

        try:
            refund_res = lahza.refund_payment(payment.provider_id, amount_minor=amount_minor)
        except lahza.LahzaError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # مبدئيًا، اعتبرها مستردة (أو بدّل حسب حالة ردّ API)
        payment.status = 'refunded'
        payment.save(update_fields=['status', 'updated_at'])

        return Response({"refund": refund_res, "status": payment.status})
