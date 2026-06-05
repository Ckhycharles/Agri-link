# Agrilink Backend

A Django REST Framework backend for the Agrilink agricultural platform. This backend provides APIs for crop management, weather monitoring, product marketplace, payments, and order management.

## Features

- **User Management**: Farmer, Buyer, Enterprise, and Admin roles
- **Farm Management**: Farm profiles with location tracking
- **Crop Management**: Track crop events, production data, and yields
- **Weather Intelligence**: Weather alerts, Sentinel imagery, and climate data
- **Marketplace**: Product listings, reviews, and ratings
- **Order Management**: Order processing, delivery tracking, and ratings
- **Payments**: M-Pesa integration, escrow system, subscriptions
- **Messaging**: Direct messages and conversations
- **Notifications**: Real-time alerts and notifications

## Tech Stack

- Django 4.2
- Django REST Framework 3.14
- MySQL 8.0
- Redis (Celery, caching)

## Prerequisites

- Python 3.9+
- MySQL 8.0+
- Redis 6+ (optional, for caching)

## Installation

### Local Development

1. **Clone and navigate to the project:**
   ```bash
   cd Agrilink-Backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/users/` - Register new user
- `POST /api/auth/token/` - Get JWT token
- `GET /api/auth/users/me/` - Get current user

### Crops
- `GET /api/crops/crops/` - List crops
- `POST /api/crops/crops/` - Create crop
- `GET /api/crops/events/` - List crop events
- `POST /api/crops/events/` - Create event

### Weather
- `GET /api/weather/alerts/` - Weather alerts
- `GET /api/weather/data/` - Weather data
- `GET /api/weather/sentinel/` - Sentinel imagery

### Products
- `GET /api/products/products/` - List products
- `POST /api/products/products/` - Create product
- `GET /api/products/products/{id}/nearby/` - Nearby products

### Orders
- `GET /api/orders/orders/` - List orders
- `POST /api/orders/orders/` - Create order
- `GET /api/orders/orders/my_purchases/` - My purchases
- `GET /api/orders/orders/my_sales/` - My sales

### Payments
- `GET /api/payments/payments/` - Payment history
- `POST /api/payments/payments/initiate_mpesa/` - Initiate M-Pesa payment

### Messages
- `GET /api/messages/messages/` - List messages
- `POST /api/messages/messages/` - Send message
- `GET /api/messages/conversations/` - List conversations

## Testing

Run tests:
```bash
python manage.py test
```

Run specific test:
```bash
python manage.py test apps.core.tests
```

## Project Structure

```
Agrilink-Backend/
├── agrilink_backend/     # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/            # User, Farm, Subscription models
│   ├── crops/           # Crop management
│   ├── weather/         # Weather data & alerts
│   ├── products/        # Marketplace
│   ├── payments/        # Payment processing
│   ├── orders/          # Order management
│   └── messages/        # Messaging & notifications
├── manage.py
├── requirements.txt
└── .env.example
```

## Environment Variables

Key environment variables to configure:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/agrilink_db
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
OPENWEATHER_API_KEY=your-weather-api-key
```

## Integrations

### M-Pesa Payment
- Configured for Kenyan market
- Implement STK Push flow in payment views

### Supabase Authentication
- Verify JWT tokens from Supabase
- Support for multiple user roles

### Weather APIs
- OpenWeather for current weather data
- Sentinel-Hub for satellite imagery

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## License

This project is part of the Agrilink platform. All rights reserved.

## Support

For issues and questions, please contact the development team or open an issue in the repository.
