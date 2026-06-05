from django.contrib import admin
from .models import Order, OrderItem, Delivery, Rating

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'seller__username', 'id')
    inlines = [OrderItemInline]

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'tracking_number', 'estimated_delivery')
    list_filter = ('status', 'created_at')
    search_fields = ('tracking_number',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('order', 'buyer_rating', 'seller_rating', 'created_at')
    list_filter = ('created_at',)
