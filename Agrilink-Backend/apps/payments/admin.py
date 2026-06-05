from django.contrib import admin
from .models import Payment, MpesaTransaction, Escrow, Subscription

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'reference_id')

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'mpesa_ref', 'receipt_number', 'created_at')
    search_fields = ('phone_number', 'mpesa_ref')

@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ('seller', 'buyer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('seller__username', 'buyer__username')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'is_active', 'renews_at')
    list_filter = ('tier', 'is_active')
    search_fields = ('user__username',)
