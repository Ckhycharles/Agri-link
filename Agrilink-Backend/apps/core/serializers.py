from rest_framework import serializers
from .models import User, Farm, Subscription, EmailVerification, PhoneVerification, GoogleOAuthToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'country', 'profile_image', 'bio', 'is_verified', 'email_verified', 'phone_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified', 'email_verified', 'phone_verified']

class UserDetailSerializer(serializers.ModelSerializer):
    farm = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'country', 'profile_image', 'bio', 'is_verified', 'email_verified', 'phone_verified', 'farm', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified', 'email_verified', 'phone_verified']
    
    def get_farm(self, obj):
        if hasattr(obj, 'farm'):
            return FarmSerializer(obj.farm).data
        return None

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'owner', 'name', 'location', 'latitude', 'longitude', 'size_hectares', 'description', 'image', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'tier', 'is_active', 'started_at', 'expires_at', 'auto_renew']
        read_only_fields = ['id', 'user', 'started_at']


# Authentication Serializers

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['user', 'token', 'is_verified', 'created_at', 'expires_at']
        read_only_fields = ['token', 'created_at', 'expires_at']


class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ['user', 'phone_number', 'is_verified', 'attempts', 'created_at', 'expires_at']
        read_only_fields = ['otp_code', 'attempts', 'created_at', 'expires_at']


class GoogleOAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleOAuthToken
        fields = ['user', 'access_token', 'refresh_token', 'id_token', 'token_type', 'expires_at', 'created_at']
        read_only_fields = ['user', 'created_at']


class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class SendPhoneOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class VerifyPhoneOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(max_length=6)


class GoogleSignInSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    access_token = serializers.CharField(required=False)
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    picture = serializers.URLField(required=False)
    role = serializers.CharField(default='farmer', required=False)
