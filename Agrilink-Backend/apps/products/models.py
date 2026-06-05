from django.db import models
from apps.core.models import User, Farm

class Product(models.Model):
    PRODUCT_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('sold_out', 'Sold Out'),
    )
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Price per unit')
    quantity_available = models.IntegerField()
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Available stock quantity')
    unit = models.CharField(max_length=50, default='kg')  # kg, liters, pieces, etc.
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    cover_image_url = models.URLField(blank=True, help_text='URL to cover image')
    image_emoji = models.CharField(max_length=10, blank=True, default='📦', help_text='Emoji representation of product')
    video_url = models.URLField(blank=True, help_text='URL to product video')
    is_organic = models.BooleanField(default=False, help_text='Is this product organic?')
    is_available = models.BooleanField(default=True, help_text='Is product currently available?')
    location = models.CharField(max_length=255, blank=True, help_text='Location where product is produced')
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS_CHOICES, default='active')
    rating = models.FloatField(default=0)  # 0-5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'reviewer')
    
    def __str__(self):
        return f"Review for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
