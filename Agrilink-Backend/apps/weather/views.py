from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import WeatherAlert, WeatherData, SentinelImagery
from .serializers import WeatherAlertSerializer, WeatherDataSerializer, SentinelImagerySerializer

class WeatherAlertViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherAlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return WeatherAlert.objects.filter(farm__owner=user)

class WeatherDataViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return WeatherData.objects.filter(farm__owner=user)

class SentinelImageryViewSet(viewsets.ModelViewSet):
    serializer_class = SentinelImagerySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return SentinelImagery.objects.filter(farm__owner=user)
