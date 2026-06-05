from django.db import models
from apps.core.models import User

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('mpesa', 'M-Pesa'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency}"

class MpesaTransaction(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='mpesa')
    phone_number = models.CharField(max_length=20)
    mpesa_ref = models.CharField(max_length=255, unique=True)
    receipt_number = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"M-Pesa: {self.mpesa_ref}"

class Escrow(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('released', 'Released'),
        ('disputed', 'Disputed'),
    )
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='escrow_seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='escrow_buyer')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Escrow: {self.seller.username} - {self.buyer.username}"

class Subscription(models.Model):
    TIER_CHOICES = (
        ('basic', 'Basic - KES 500/month'),
        ('pro', 'Pro - KES 2000/month'),
        ('enterprise', 'Enterprise - Custom'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_subscriptions')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    renews_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tier}"
