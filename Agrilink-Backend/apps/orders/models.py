from django.db import models
from apps.core.models import User
from apps.products.models import Product

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('mpesa', 'M-Pesa'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
        ('cash', 'Cash On Delivery'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='mpesa'
    )
    payment_ref = models.CharField(max_length=255, blank=True, help_text='Payment reference number')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.buyer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    recipient_address = models.TextField()
    recipient_phone = models.CharField(max_length=20)
    tracking_number = models.CharField(max_length=255, unique=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    actual_delivery = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Delivery for Order {self.order.id}"

class Rating(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='rating')
    buyer_rating = models.IntegerField(null=True, blank=True)  # 1-5
    buyer_comment = models.TextField(blank=True)
    seller_rating = models.IntegerField(null=True, blank=True)  # 1-5
    seller_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rating for Order {self.order.id}"
