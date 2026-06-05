"""
Utility functions for the Agrilink Backend
"""
from decimal import Decimal
from datetime import datetime, timedelta


def calculate_order_total(items):
    """Calculate total amount for order items"""
    total = Decimal('0.00')
    for item in items:
        total += item['price_per_unit'] * item['quantity']
    return total


def generate_tracking_number():
    """Generate a unique tracking number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    import random
    random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"AGRI-{timestamp}-{random_suffix}"


def calculate_subscription_expiry(days=30):
    """Calculate subscription expiry date"""
    return datetime.now() + timedelta(days=days)


def get_user_coordinates(user):
    """Get user's farm coordinates for location-based queries"""
    try:
        farm = user.farm
        return {
            'latitude': farm.latitude,
            'longitude': farm.longitude
        }
    except:
        return None


def distance_between_points(lat1, lon1, lat2, lon2):
    """Calculate distance between two geographical points using Haversine formula"""
    from math import radians, cos, sin, asin, sqrt
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r
