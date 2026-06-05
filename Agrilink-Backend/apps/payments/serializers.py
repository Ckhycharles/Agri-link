from rest_framework import serializers
from .models import Payment, MpesaTransaction, Escrow, Subscription

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = ['id', 'phone_number', 'mpesa_ref', 'receipt_number', 'created_at']
        read_only_fields = ['id', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    mpesa = MpesaTransactionSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'currency', 'payment_method', 'status', 'reference_id', 'description', 'mpesa', 'created_at', 'completed_at']
        read_only_fields = ['id', 'user', 'created_at', 'completed_at']

class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = ['id', 'seller', 'buyer', 'amount', 'status', 'description', 'created_at', 'released_at']
        read_only_fields = ['id', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'tier', 'is_active', 'auto_renew', 'created_at', 'renews_at']
        read_only_fields = ['id', 'user', 'created_at']
