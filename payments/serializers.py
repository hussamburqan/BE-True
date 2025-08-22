from rest_framework import serializers
from .models import Payment


class PaymentCreateSerializer(serializers.Serializer):
    amount   = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(default='ILS', max_length=10)
    email    = serializers.EmailField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)


class PaymentVerifySerializer(serializers.Serializer):
    provider_id = serializers.CharField()


class RefundSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    amount     = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = ['id', 'provider', 'provider_id', 'amount', 'currency', 'status', 'checkout_url', 'created_at']
