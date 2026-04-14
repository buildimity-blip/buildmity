import os
from decouple import config

# MTN Mobile Money API Configuration
MTN_CONFIG = {
    'api_url': config('MTN_API_URL', default='https://sandbox.mtn.com/api/'),
    'api_key': config('MTN_API_KEY', default=''),
    'api_secret': config('MTN_API_SECRET', default=''),
    'callback_url': config('MTN_CALLBACK_URL', default='https://yourdomain.com/api/mtn-callback/'),
    'environment': config('MTN_ENVIRONMENT', default='sandbox'),  # sandbox or production
}

# Airtel Money API Configuration
AIRTEL_CONFIG = {
    'api_url': config('AIRTEL_API_URL', default='https://openapi.airtel.africa/'),
    'client_id': config('AIRTEL_CLIENT_ID', default=''),
    'client_secret': config('AIRTEL_CLIENT_SECRET', default=''),
    'callback_url': config('AIRTEL_CALLBACK_URL', default='https://yourdomain.com/api/airtel-callback/'),
    'environment': config('AIRTEL_ENVIRONMENT', default='sandbox'),
}

# Payment Settings
PAYMENT_SETTINGS = {
    'platform_fee_percentage': 10,  # 10% platform fee
    'minimum_payment': 1000,  # Minimum UGX 1000
    'maximum_payment': 5000000,  # Maximum UGX 5,000,000
}