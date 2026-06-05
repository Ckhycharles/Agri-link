from rest_framework import serializers
from .models import Product, ProductReview, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']

class ProductReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'reviewer', 'reviewer_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'reviewer', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.username', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'farmer', 'farmer_name', 'name', 'description', 'category', 'price', 'quantity_available', 'unit', 'image', 'status', 'rating', 'images', 'reviews', 'created_at', 'updated_at']
        read_only_fields = ['id', 'farmer', 'created_at', 'updated_at']
