from django.contrib import admin
from .models import User, Farm, Subscription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'size_hectares', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'location', 'owner__username')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'is_active', 'expires_at')
    list_filter = ('tier', 'is_active')
    search_fields = ('user__username',)
