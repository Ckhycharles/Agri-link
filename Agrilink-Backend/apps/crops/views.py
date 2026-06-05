from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Crop, CropEvent, CropProduction
from .serializers import CropSerializer, CropEventSerializer, CropProductionSerializer
from apps.core.models import Farm

class CropViewSet(viewsets.ModelViewSet):
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Crop.objects.filter(farm__owner=user)
    
    def perform_create(self, serializer):
        farm = Farm.objects.get(owner=self.request.user)
        serializer.save(farm=farm)
    
    @action(detail=True, methods=['post'])
    def mark_done(self, request, pk=None):
        crop = self.get_object()
        event = CropEvent.objects.create(
            crop=crop,
            event_type='other',
            title='Status updated',
            date=request.data.get('date'),
            done=True
        )
        return Response({'status': 'event created'})

class CropEventViewSet(viewsets.ModelViewSet):
    serializer_class = CropEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return CropEvent.objects.filter(crop__farm__owner=user)
    
    def perform_create(self, serializer):
        crop_id = self.request.data.get('crop')
        crop = Crop.objects.get(id=crop_id, farm__owner=self.request.user)
        serializer.save(crop=crop)

class CropProductionViewSet(viewsets.ModelViewSet):
    serializer_class = CropProductionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return CropProduction.objects.filter(crop__farm__owner=user)
