# Quick Start Guide

## Getting Started with Agrilink Backend

### 1. Initial Setup (Windows)

```bash
# Navigate to the project directory
cd c:\Users\Admin\Desktop\project1\Agrilink-Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your settings:
- `DEBUG=True` (for development)
- `SECRET_KEY=your-secret-key-change-in-production`
- Database credentials
- API keys for M-Pesa, Weather, etc.

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`
Admin panel at: `http://localhost:8000/admin/`

### 5. Testing the API

Visit these endpoints:
- Get current user: `GET http://localhost:8000/api/auth/users/me/`
- List crops: `GET http://localhost:8000/api/crops/crops/`
- List products: `GET http://localhost:8000/api/products/products/`

## API Documentation

### Base URL
- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

### Authentication
All endpoints (except registration) require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Main API Routes

**Auth & Users**
- `POST /auth/users/` - Register
- `POST /auth/token/` - Login (get JWT token)
- `GET /auth/users/me/` - Current user profile

**Crops**
- `GET /crops/crops/` - List your crops
- `POST /crops/crops/` - Create crop
- `GET /crops/events/` - Crop events
- `POST /crops/events/` - Create event

**Products**
- `GET /products/products/` - List all products
- `POST /products/products/` - Create product
- `GET /products/products/{id}/` - Product detail
- `GET /products/products/{id}/nearby/` - Nearby products

**Orders**
- `GET /orders/orders/` - List orders
- `GET /orders/orders/my_purchases/` - Buyer's purchases
- `GET /orders/orders/my_sales/` - Seller's sales

**Payments**
- `GET /payments/payments/` - Payment history
- `POST /payments/payments/initiate_mpesa/` - Initiate M-Pesa payment

**Weather**
- `GET /weather/alerts/` - Weather alerts for your farm
- `GET /weather/data/` - Historical weather data

**Messages**
- `GET /messages/messages/` - All messages
- `POST /messages/messages/` - Send message
- `GET /messages/conversations/` - Your conversations

## Integration with Frontend

Update your frontend's API configuration to point to your Django backend:

In frontend `.env`:
```
VITE_API_URL=http://localhost:8000/api
```

Update CORS settings in Django if running on different ports:
```python
CORS_ALLOWED_ORIGINS=[
    "http://localhost:3000",
    "http://localhost:5173",
]
```

## Database Backup

```bash
# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json
```

## Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check
```

## Troubleshooting

### Port Already in Use
```bash
# Change port
python manage.py runserver 8001
```

### Database Connection Error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Clear Cache
```bash
# Clear Django cache
python manage.py clear_cache
```

## Next Steps

1. **Connect Frontend**: Update frontend API URL to point to this backend
2. **Configure External APIs**: Add M-Pesa, Weather, and other API credentials
3. **Set up Email**: Configure email backend for notifications
4. **Deploy**: Follow deployment guide for production setup
5. **Monitor**: Set up logging and monitoring

## Support

For detailed documentation, see [README.md](./README.md)
For API documentation, visit Django admin at `/admin/`

Enjoy building Agrilink! 🌾🚀
