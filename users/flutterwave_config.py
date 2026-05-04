import os
from decouple import config

FLUTTERWAVE_CONFIG = {
    'public_key': config('FLUTTERWAVE_PUBLIC_KEY', default=''),
    'secret_key': config('FLUTTERWAVE_SECRET_KEY', default=''),
    'encryption_key': config('FLUTTERWAVE_ENCRYPTION_KEY', default=''),
    'environment': config('FLUTTERWAVE_ENVIRONMENT', default='sandbox'),
    'callback_url': config('FLUTTERWAVE_CALLBACK_URL', default='http://127.0.0.1:8000/api/flutterwave-webhook/'),
}
# Payment Methods
PAYMENT_METHODS = {
    'mtn': 'MTN Mobile Money Uganda',
    'airtel': 'Airtel Money Uganda',
    'card': 'Card Payment',
    'bank_transfer': 'Bank Transfer',
}

# Transaction Fees
TRANSACTION_FEES = {
    'percentage': 1.4,  # 1.4% + UGX 100
    'fixed': 100,
}