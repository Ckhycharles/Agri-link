from rest_framework import serializers
from .models import Crop, CropEvent, CropProduction

class CropEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropEvent
        fields = ['id', 'crop', 'event_type', 'title', 'date', 'time', 'description', 'done', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']

class CropProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropProduction
        fields = ['id', 'crop', 'expected_yield', 'actual_yield', 'yield_unit', 'harvest_date', 'quality_rating', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']

class CropSerializer(serializers.ModelSerializer):
    events = CropEventSerializer(many=True, read_only=True)
    production = CropProductionSerializer(read_only=True)
    
    class Meta:
        model = Crop
        fields = ['id', 'farm', 'name', 'crop_type', 'variety', 'planting_date', 'expected_harvest_date', 'area_hectares', 'quantity_planted', 'unit', 'status', 'notes', 'image', 'events', 'production', 'created_at', 'updated_at']
        read_only_fields = ['id', 'farm', 'created_at', 'updated_at']
