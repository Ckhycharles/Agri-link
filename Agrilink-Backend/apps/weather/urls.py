from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherAlertViewSet, WeatherDataViewSet, SentinelImageryViewSet

router = DefaultRouter()
router.register(r'alerts', WeatherAlertViewSet, basename='weather-alert')
router.register(r'data', WeatherDataViewSet, basename='weather-data')
router.register(r'sentinel', SentinelImageryViewSet, basename='sentinel')

urlpatterns = [
    path('', include(router.urls)),
]
