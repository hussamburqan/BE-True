# payments/urls.py
from django.urls import path
from .callback import lahza_callback  
from .views import (
    PaymentCreateView,
    PaymentVerifyView,
    PaymentHistoryView,
    PaymentRefundView,
)

urlpatterns = [
    path('create',  PaymentCreateView.as_view(),  name='payment-create'),
    path('verify',  PaymentVerifyView.as_view(),  name='payment-verify'),
    path('history', PaymentHistoryView.as_view(), name='payment-history'),
    path('refund',  PaymentRefundView.as_view(),  name='payment-refund'),
    path('callback/', lahza_callback,             name='lahza-callback'), 

]
