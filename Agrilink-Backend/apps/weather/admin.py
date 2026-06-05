from django.contrib import admin
from .models import WeatherAlert, WeatherData, SentinelImagery

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'farm', 'alert_type', 'severity', 'date')
    list_filter = ('alert_type', 'severity', 'date')
    search_fields = ('title', 'farm__name')

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('farm', 'date', 'temperature', 'humidity', 'condition')
    list_filter = ('date',)
    search_fields = ('farm__name',)

@admin.register(SentinelImagery)
class SentinelImageryAdmin(admin.ModelAdmin):
    list_display = ('farm', 'date', 'ndvi', 'cloud_cover')
    list_filter = ('date',)
    search_fields = ('farm__name',)
