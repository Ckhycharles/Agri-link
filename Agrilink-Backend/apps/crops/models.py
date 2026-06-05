from django.db import models
from apps.core.models import User, Farm

class Crop(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=255)
    crop_type = models.CharField(max_length=100)
    variety = models.CharField(max_length=255, blank=True)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    area_hectares = models.FloatField()
    quantity_planted = models.FloatField()
    unit = models.CharField(max_length=50, default='kg')
    status = models.CharField(max_length=50, choices=[
        ('planning', 'Planning'),
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('ready', 'Ready to Harvest'),
        ('harvested', 'Harvested'),
    ], default='planning')
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.farm.name}"

class CropEvent(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=100, choices=[
        ('planting', 'Planting'),
        ('watering', 'Watering'),
        ('fertilizing', 'Fertilizing'),
        ('spraying', 'Spraying'),
        ('weeding', 'Weeding'),
        ('harvesting', 'Harvesting'),
        ('other', 'Other'),
    ])
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.crop.name}"

class CropProduction(models.Model):
    crop = models.OneToOneField(Crop, on_delete=models.CASCADE, related_name='production')
    expected_yield = models.FloatField()
    actual_yield = models.FloatField(null=True, blank=True)
    yield_unit = models.CharField(max_length=50, default='kg')
    harvest_date = models.DateField(null=True, blank=True)
    quality_rating = models.IntegerField(null=True, blank=True)  # 1-5
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Production - {self.crop.name}"
