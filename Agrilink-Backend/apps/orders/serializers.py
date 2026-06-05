from rest_framework import serializers
from .models import Order, OrderItem, Delivery, Rating

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_per_unit', 'total_price']

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'status', 'recipient_address', 'recipient_phone', 'tracking_number', 'estimated_delivery', 'actual_delivery', 'created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'buyer_rating', 'buyer_comment', 'seller_rating', 'seller_comment', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery = DeliverySerializer(read_only=True)
    rating = RatingSerializer(read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'buyer_name', 'seller', 'seller_name', 'status', 'total_amount', 'notes', 'items', 'delivery', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'buyer', 'seller', 'total_amount', 'created_at', 'updated_at']
