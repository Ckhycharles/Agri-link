from rest_framework import serializers
from .models import WeatherAlert, WeatherData, SentinelImagery

class WeatherAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherAlert
        fields = ['id', 'farm', 'alert_type', 'title', 'description', 'severity', 'recommendation', 'date', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['id', 'farm', 'date', 'temperature', 'humidity', 'rainfall', 'wind_speed', 'uv_index', 'condition', 'created_at']
        read_only_fields = ['id', 'created_at']

class SentinelImagerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SentinelImagery
        fields = ['id', 'farm', 'ndvi', 'cloud_cover', 'image_url', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
