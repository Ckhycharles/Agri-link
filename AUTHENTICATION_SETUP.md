# Authentication Enhancement Guide

This document explains how to implement and use the new authentication features:
- Email Verification
- Phone OTP (SMS)
- Google Sign-In

## Setup Instructions

### 1. Backend Setup

#### Install Dependencies
```bash
pip install -r requirements.txt
```

The following new packages have been added:
- `google-auth` - Google authentication
- `google-auth-oauthlib` - OAuth support
- `django-allauth` - Third-party auth support
- `social-auth-app-django` - Social authentication
- `python-jose` - JWT token handling

#### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

This creates tables for:
- `EmailVerification` - Email verification tokens
- `PhoneVerification` - Phone OTP records
- `GoogleOAuthToken` - Google OAuth token storage

#### Configure Environment Variables

Update `.env` file with:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Gmail app password, not regular password
DEFAULT_FROM_EMAIL=noreply@agrilink.com

# Frontend URL for email links
FRONTEND_URL=http://localhost:5173

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

# Twilio (for SMS OTP)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio phone number
```

### 2. Email Configuration (Gmail Example)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "Less secure app access" or use App Passwords
3. Create an App Password for your Gmail account
4. Use this password in `EMAIL_HOST_PASSWORD`

Alternatively, use SendGrid, Mailgun, or other SMTP providers.

### 3. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized origins:
   - `http://localhost:5173` (development)
   - `your-production-domain.com` (production)
6. Add authorized redirect URIs:
   - `http://localhost:5173/auth/google-callback`
   - `your-production-domain.com/auth/google-callback`
7. Copy the Client ID and Secret to your `.env`

### 4. Twilio Setup (for Phone OTP)

1. Go to [Twilio Console](https://www.twilio.com/console)
2. Create a new phone number or use existing
3. Copy Account SID and Auth Token
4. Add credentials to `.env`

## Frontend Integration

### 1. Update Vite Environment Variables

Create or update `.env.local`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

### 2. Use Authentication Services

#### Email Verification Example
```typescript
import { sendEmailVerification, verifyEmail } from '@/lib/authService';

// Send verification email
await sendEmailVerification('user@example.com');

// Verify with token (from email link)
await verifyEmail(token);
```

#### Phone OTP Example
```typescript
import { sendPhoneOTP, verifyPhoneOTP } from '@/lib/authService';

// Send OTP to phone
await sendPhoneOTP('+254712345678');

// Verify OTP
await verifyPhoneOTP('+254712345678', '123456');
```

#### Google Sign-In Example
```typescript
import { GoogleSignInButton } from '@/components/auth/GoogleSignInButton';

<GoogleSignInButton role="farmer" onSuccess={handleSuccess} />
```

### 3. Use UI Components

#### EmailVerificationForm
```tsx
import { EmailVerificationForm } from '@/components/auth/EmailVerificationForm';

<EmailVerificationForm onSuccess={handleSuccess} onError={handleError} />
```

#### PhoneOTPForm
```tsx
import { PhoneOTPForm } from '@/components/auth/PhoneOTPForm';

<PhoneOTPForm onSuccess={handleSuccess} onError={handleError} />
```

#### GoogleSignInButton
```tsx
import { GoogleSignInButton } from '@/components/auth/GoogleSignInButton';

<GoogleSignInButton role="farmer" onSuccess={handleSuccess} />
```

## API Endpoints

### Email Verification
- **POST** `/api/auth/send_email_verification/` - Send verification email
- **POST** `/api/auth/verify_email/` - Verify email with token

### Phone OTP
- **POST** `/api/auth/send_phone_otp/` - Send OTP to phone
- **POST** `/api/auth/verify_phone_otp/` - Verify OTP code

### Google Sign-In
- **POST** `/api/auth/google_signin/` - Google token exchange and user creation

## Database Schema

### EmailVerification Model
```
- user: OneToOneField(User)
- token: CharField (unique, UUID)
- is_verified: BooleanField
- created_at: DateTimeField (auto_now_add)
- expires_at: DateTimeField (24 hours)
```

### PhoneVerification Model
```
- user: OneToOneField(User)
- phone_number: CharField
- otp_code: CharField (6 digits)
- is_verified: BooleanField
- attempts: IntegerField (max 3)
- created_at: DateTimeField (auto_now_add)
- expires_at: DateTimeField (10 minutes)
```

### GoogleOAuthToken Model
```
- user: OneToOneField(User)
- access_token: TextField
- refresh_token: TextField
- id_token: TextField
- token_type: CharField (default: Bearer)
- expires_at: DateTimeField
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)
```

## User Model Updates

New fields added to User model:
- `email_verified: BooleanField` - Tracks email verification status
- `phone_verified: BooleanField` - Tracks phone verification status
- `google_id: CharField` - Google account ID (unique, nullable)

## Security Considerations

1. **Email Tokens**: Expire after 24 hours
2. **OTP Codes**: 6-digit codes, expire after 10 minutes
3. **Attempt Limiting**: Max 3 failed OTP attempts
4. **HTTPS Only**: Use HTTPS in production
5. **CORS**: Configure appropriate CORS origins in settings.py
6. **Token Storage**: Use httpOnly cookies in production (not localStorage)

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Resource created (Google Sign-In new user)
- `400` - Bad request/Validation error
- `401` - Unauthorized
- `404` - Not found
- `429` - Too many requests (rate limiting)
- `500` - Server error

## Testing

### Manual Testing
1. Start Django server: `python manage.py runserver`
2. Start React dev server: `npm run dev`
3. Test each authentication method in browser

### Unit Tests
Submit tests for each endpoint and service function.

## Troubleshooting

### Email Not Sending
- Check EMAIL_BACKEND in settings.py
- Verify SMTP credentials in .env
- Check Gmail app passwords if using Gmail
- Look for logs in Django console

### OTP Not Sending
- Verify Twilio credentials
- Check phone number format (+country code required)
- Ensure Twilio account has sufficient balance
- Check Twilio logs in console

### Google Sign-In Not Working
- Verify GOOGLE_OAUTH_CLIENT_ID is set
- Check Google Cloud Console OAuth configuration
- Verify redirect URIs match frontend URL
- Check browser console for JS errors

## Future Enhancements

1. Add email verification requirement before login
2. Add phone verification requirement for farmers
3. Support multiple phone numbers per user
4. Add 2FA (Two-Factor Authentication)
5. Support other OAuth providers (GitHub, Apple, Facebook)
6. Implement biometric authentication
7. Add passwordless email sign-in links
8. Rate limiting on OTP requests

## References

- [Django Email Configuration](https://docs.djangoproject.com/en/4.2/topics/email/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Twilio SMS Documentation](https://www.twilio.com/docs/sms)
- [JWT Token Structure](https://jwt.io/)
