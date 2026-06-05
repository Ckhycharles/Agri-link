from django.contrib import admin
from .models import Crop, CropEvent, CropProduction

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'farm', 'status', 'planting_date', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'farm__name')

@admin.register(CropEvent)
class CropEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'crop', 'event_type', 'date', 'done')
    list_filter = ('event_type', 'done', 'date')
    search_fields = ('title', 'crop__name')

@admin.register(CropProduction)
class CropProductionAdmin(admin.ModelAdmin):
    list_display = ('crop', 'expected_yield', 'actual_yield', 'quality_rating')
    list_filter = ('created_at',)
    search_fields = ('crop__name',)
