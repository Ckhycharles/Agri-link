from django.db import models
from apps.core.models import Farm

class WeatherAlert(models.Model):
    ALERT_TYPE_CHOICES = (
        ('drought', 'Drought'),
        ('flood', 'Flood'),
        ('pest', 'Pest Attack'),
        ('disease', 'Disease'),
        ('frost', 'Frost'),
        ('heatwave', 'Heatwave'),
        ('other', 'Other'),
    )
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_alerts')
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    recommendation = models.TextField()
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.farm.name}"

class WeatherData(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateField()
    temperature = models.FloatField()  # Celsius
    humidity = models.FloatField()  # Percentage
    rainfall = models.FloatField(default=0)  # mm
    wind_speed = models.FloatField()  # km/h
    uv_index = models.IntegerField()
    condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ('farm', 'date')
    
    def __str__(self):
        return f"Weather - {self.farm.name} - {self.date}"

class SentinelImagery(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='sentinel_imagery')
    ndvi = models.FloatField()  # Normalized Difference Vegetation Index
    cloud_cover = models.FloatField()  # Percentage
    image_url = models.URLField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Sentinel - {self.farm.name} - {self.date}"
