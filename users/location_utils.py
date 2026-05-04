import math
from decimal import Decimal
from django.db.models import Q
import requests
import os

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers using Haversine formula"""
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    R = 6371  # Earth's radius in kilometers
    
    try:
        lat1_rad = math.radians(float(lat1))
        lon1_rad = math.radians(float(lon1))
        lat2_rad = math.radians(float(lat2))
        lon2_rad = math.radians(float(lon2))
        
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return round(R * c, 2)
    except Exception as e:
        print(f"Distance calculation error: {e}")
        return None


def calculate_eta(distance_km, speed_kmh=30):
    """Calculate estimated time of arrival in minutes"""
    if distance_km is None or distance_km <= 0:
        return None
    return int((distance_km / speed_kmh) * 60)


def find_nearby_providers(latitude, longitude, radius_km=10, service_id=None):
    """Find providers within specified radius"""
    from .models import User
    
    if not latitude or not longitude:
        return []
    
    providers = User.objects.filter(
        role='provider',
        is_verified=True,
        is_active=True,
        is_suspended=False,
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    if service_id:
        providers = providers.filter(service_id=service_id)
    
    nearby = []
    for provider in providers:
        if provider.latitude and provider.longitude:
            try:
                distance = calculate_distance(
                    float(latitude), float(longitude),
                    float(provider.latitude), float(provider.longitude)
                )
                if distance is not None and distance <= radius_km:
                    nearby.append({
                        'provider': provider,
                        'distance': distance,
                        'eta': calculate_eta(distance)
                    })
            except Exception as e:
                print(f"Error processing provider {provider.id}: {e}")
                continue
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance'])
    return nearby


def calculate_trip_price(distance_km, service_type='standard'):
    """Calculate price based on distance"""
    if distance_km is None:
        return 5000
    
    base_price = 5000  # Base fare in UGX
    per_km_rate = 2000  # Per km rate
    total_price = base_price + (distance_km * per_km_rate)
    
    # Adjust for service type
    if service_type == 'premium':
        total_price *= 1.5
    elif service_type == 'economy':
        total_price *= 0.8
    
    return round(total_price)


def get_address_from_coords(latitude, longitude, api_key=None):
    """Reverse geocoding to get address from coordinates"""
    if not latitude or not longitude:
        return None
    
    api_key = api_key or os.environ.get('GOOGLE_MAPS_API_KEY', '')
    if not api_key:
        return None
    
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] == 'OK' and data['results']:
            return data['results'][0]['formatted_address']
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None


def get_coords_from_address(address, api_key=None):
    """Geocode address to coordinates"""
    if not address:
        return None
    
    api_key = api_key or os.environ.get('GOOGLE_MAPS_API_KEY', '')
    if not api_key:
        return None
    
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return {
                'latitude': location['lat'],
                'longitude': location['lng'],
                'formatted_address': data['results'][0]['formatted_address']
            }
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None