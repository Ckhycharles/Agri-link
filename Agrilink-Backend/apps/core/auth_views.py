from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import json
import uuid
from jose import jwt, JWTClaimError, JWTError

from .models import User, EmailVerification, PhoneVerification, GoogleOAuthToken
from .serializers import (
    UserDetailSerializer,
    SendEmailVerificationSerializer,
    VerifyEmailSerializer,
    SendPhoneOTPSerializer,
    VerifyPhoneOTPSerializer,
    GoogleSignInSerializer,
)


class AuthViewSet(viewsets.ViewSet):
    """
    Authentication endpoints for email verification, phone OTP, and Google Sign-In
    """
    
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def send_email_verification(self, request):
        """Send email verification link"""
        serializer = SendEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User with this email does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create or update email verification
        email_verification, created = EmailVerification.objects.get_or_create(
            user=user,
            defaults={'expires_at': timezone.now() + timedelta(hours=24)}
        )
        
        if not created:
            email_verification.token = str(uuid.uuid4())
            email_verification.expires_at = timezone.now() + timedelta(hours=24)
            email_verification.save()
        
        # Send verification email
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={email_verification.token}"
        try:
            send_mail(
                subject='Verify your Agrilink email',
                message=f'Click the link to verify your email: {verification_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=f'''
                    <h2>Email Verification</h2>
                    <p>Click the link below to verify your Agrilink account:</p>
                    <a href="{verification_url}">Verify Email</a>
                    <p>This link expires in 24 hours.</p>
                '''
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(
            {'message': 'Verification email sent successfully'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        """Verify email with token"""
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            email_verification = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid verification token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if email_verification.is_expired():
            return Response(
                {'error': 'Verification token has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark email as verified
        user = email_verification.user
        user.email_verified = True
        user.save()
        
        email_verification.is_verified = True
        email_verification.save()
        
        return Response(
            {
                'message': 'Email verified successfully',
                'user': UserDetailSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def send_phone_otp(self, request):
        """Send OTP to phone number"""
        serializer = SendPhoneOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {'error': 'User with this phone number does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Create or update phone verification
        phone_verification, created = PhoneVerification.objects.get_or_create(
            user=user,
            defaults={
                'phone_number': phone_number,
                'otp_code': otp_code,
                'expires_at': timezone.now() + timedelta(minutes=10)
            }
        )
        
        if not created:
            if phone_verification.is_locked():
                return Response(
                    {'error': 'Too many failed attempts. Try again later.'},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            phone_verification.otp_code = otp_code
            phone_verification.attempts = 0
            phone_verification.expires_at = timezone.now() + timedelta(minutes=10)
            phone_verification.save()
        
        # Send OTP via Twilio
        try:
            from twilio.rest import Client
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            twilio_client.messages.create(
                body=f'Your Agrilink verification code is: {otp_code}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send OTP: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(
            {'message': 'OTP sent to phone number'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def verify_phone_otp(self, request):
        """Verify phone with OTP"""
        serializer = VerifyPhoneOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']
        
        try:
            phone_verification = PhoneVerification.objects.get(phone_number=phone_number)
        except PhoneVerification.DoesNotExist:
            return Response(
                {'error': 'OTP not found for this phone number'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if phone_verification.is_expired():
            return Response(
                {'error': 'OTP has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if phone_verification.is_locked():
            return Response(
                {'error': 'Too many failed attempts. Request a new OTP.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        if phone_verification.otp_code != otp_code:
            phone_verification.attempts += 1
            phone_verification.save()
            return Response(
                {'error': 'Invalid OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark phone as verified
        user = phone_verification.user
        user.phone_verified = True
        user.save()
        
        phone_verification.is_verified = True
        phone_verification.attempts = 0
        phone_verification.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'message': 'Phone verified successfully',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                },
                'user': UserDetailSerializer(user).data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def google_signin(self, request):
        """Google Sign-In endpoint"""
        serializer = GoogleSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        id_token = serializer.validated_data['id_token']
        email = serializer.validated_data['email']
        google_id = serializer.validated_data.get('google_id') or email
        
        try:
            # Verify and decode Google ID token
            # NOTE: In production, verify with Google's public keys
            # For now, we'll just extract the payload
            decoded_token = self._decode_google_token(id_token)
        except (JWTError, JWTClaimError):
            return Response(
                {'error': 'Invalid Google token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user exists
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': serializer.validated_data.get('first_name', ''),
                'last_name': serializer.validated_data.get('last_name', ''),
                'google_id': google_id,
                'role': serializer.validated_data.get('role', 'farmer'),
                'email_verified': True,
                'photo_url': serializer.validated_data.get('picture', '')
            }
        )
        
        if not created:
            # Update google_id if not already set
            if not user.google_id:
                user.google_id = google_id
                user.save()
        
        # Store Google OAuth token
        GoogleOAuthToken.objects.update_or_create(
            user=user,
            defaults={
                'access_token': serializer.validated_data.get('access_token', ''),
                'id_token': id_token,
                'expires_at': timezone.now() + timedelta(hours=1)
            }
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'message': 'Google Sign-In successful',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                },
                'user': UserDetailSerializer(user).data
            },
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
        )

    def _decode_google_token(self, token):
        """
        Decode Google JWT token
        In production, verify with Google's public keys
        """
        # For development, we'll do basic validation
        try:
            # Bypass verification for now (use verify=False)
            # In production, fetch Google's public keys and verify properly
            parts = token.split('.')
            if len(parts) != 3:
                raise JWTError('Invalid token format')
            
            # This is a simplified version - in production use google-auth library
            # to verify against Google's public keys
            return True
        except Exception as e:
            raise JWTError(f'Token decode failed: {str(e)}')
