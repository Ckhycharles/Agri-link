from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('enterprise', 'Enterprise'),
        ('admin', 'Admin'),
    )
    
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='farmer')
    country = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True, help_text='County/Region information')
    farm_size = models.CharField(max_length=100, blank=True, help_text='Size of farm (e.g., "2 hectares")')
    main_crops = models.TextField(blank=True, help_text='Comma-separated list of main crops')
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    photo_url = models.URLField(blank=True, help_text='URL to profile photo')
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, blank=True, unique=True, null=True, help_text='Google OAuth ID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='agrilink_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='agrilink_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Email verification for {self.user.email}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


class PhoneVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_verification')
    phone_number = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Phone verification for {self.user.email}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_locked(self):
        return self.attempts >= self.max_attempts


class GoogleOAuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='google_oauth_token')
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True)
    id_token = models.TextField()
    token_type = models.CharField(max_length=50, default='Bearer')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Google OAuth token for {self.user.email}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


class Farm(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farm')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    size_hectares = models.FloatField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='farms/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Subscription(models.Model):
    TIER_CHOICES = (
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='free')
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tier}"


class IdVerification(models.Model):
    VERIFICATION_STATUS_CHOICES = (
        ('unverified', 'Unverified'),
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='id_verification')
    document_url = models.URLField(blank=True, help_text='URL to identity document image')
    status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='unverified'
    )
    reviewer_note = models.TextField(blank=True, help_text='Notes from verification reviewer')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"ID Verification - {self.user.username} ({self.status})"
