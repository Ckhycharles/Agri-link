from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CropViewSet, CropEventViewSet, CropProductionViewSet

router = DefaultRouter()
router.register(r'crops', CropViewSet, basename='crop')
router.register(r'events', CropEventViewSet, basename='crop-event')
router.register(r'production', CropProductionViewSet, basename='crop-production')

urlpatterns = [
    path('', include(router.urls)),
]
