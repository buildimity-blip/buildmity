import requests
import json
import hashlib
import hmac
import uuid
import base64
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from .payment_config import MTN_CONFIG, AIRTEL_CONFIG, PAYMENT_SETTINGS


class MTNMoneyGateway:
    """MTN Mobile Money Payment Gateway Integration"""
    
    def __init__(self):
        self.api_url = MTN_CONFIG['api_url']
        self.api_key = MTN_CONFIG['api_key']
        self.api_secret = MTN_CONFIG['api_secret']
        self.callback_url = MTN_CONFIG['callback_url']
        self.environment = MTN_CONFIG['environment']
    
    def get_access_token(self):
        """Get OAuth access token from MTN"""
        try:
            auth_string = f"{self.api_key}:{self.api_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_auth}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.api_url}/v1_0/apiuser/{self.api_key}/apikey",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('access_token')
            return None
        except Exception as e:
            print(f"MTN Token Error: {e}")
            return None
    
    def initiate_payment(self, phone_number, amount, reference, user_id):
        """Initiate MTN Mobile Money payment"""
        
        # Format phone number (remove leading 0, add 256)
        if phone_number.startswith('0'):
            phone_number = '256' + phone_number[1:]
        
        token = self.get_access_token()
        if not token:
            return {
                'success': False,
                'message': 'Could not authenticate with MTN. Please try again.'
            }
        
        # Prepare payment data
        payment_data = {
            'amount': str(amount),
            'currency': 'UGX',
            'externalId': reference,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': phone_number
            },
            'payerMessage': f'Payment for service request {reference}',
            'payeeNote': f'Buildimity payment - {reference}'
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'X-Reference-Id': str(uuid.uuid4()),
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/v1_0/collection/v1_0/requesttopay",
                headers=headers,
                json=payment_data,
                timeout=30
            )
            
            if response.status_code == 202:
                return {
                    'success': True,
                    'transaction_id': payment_data['externalId'],
                    'status': 'pending',
                    'message': f'Payment request sent to {phone_number}. Please check your phone.',
                    'payment_method': 'MTN Mobile Money'
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment initiation failed: {response.text}'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Payment error: {str(e)}'
            }
    
    def check_payment_status(self, transaction_id):
        """Check payment status"""
        token = self.get_access_token()
        if not token:
            return {'status': 'unknown', 'message': 'Cannot verify payment'}
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/v1_0/collection/v1_0/requesttopay/{transaction_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                return {
                    'status': status.lower(),
                    'message': f'Payment {status}',
                    'data': data
                }
            return {'status': 'unknown', 'message': 'Could not verify payment'}
        except Exception as e:
            return {'status': 'unknown', 'message': str(e)}


class AirtelMoneyGateway:
    """Airtel Money Payment Gateway Integration"""
    
    def __init__(self):
        self.api_url = AIRTEL_CONFIG['api_url']
        self.client_id = AIRTEL_CONFIG['client_id']
        self.client_secret = AIRTEL_CONFIG['client_secret']
        self.callback_url = AIRTEL_CONFIG['callback_url']
        self.environment = AIRTEL_CONFIG['environment']
    
    def get_access_token(self):
        """Get OAuth access token from Airtel"""
        try:
            auth_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(
                f"{self.api_url}/auth/oauth2/token",
                json=auth_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('access_token')
            return None
        except Exception as e:
            print(f"Airtel Token Error: {e}")
            return None
    
    def initiate_payment(self, phone_number, amount, reference, user_id):
        """Initiate Airtel Money payment"""
        
        # Format phone number
        if phone_number.startswith('0'):
            phone_number = '256' + phone_number[1:]
        
        token = self.get_access_token()
        if not token:
            return {
                'success': False,
                'message': 'Could not authenticate with Airtel. Please try again.'
            }
        
        payment_data = {
            'reference': reference,
            'subscriber': {
                'country': 'UG',
                'currency': 'UGX',
                'msisdn': phone_number
            },
            'transaction': {
                'amount': str(amount),
                'country': 'UG',
                'currency': 'UGX',
                'id': reference
            },
            'requestedAmount': str(amount),
            'country': 'UG',
            'currency': 'UGX'
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Country': 'UG',
            'X-Currency': 'UGX'
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/standard/v1/payments/",
                headers=headers,
                json=payment_data,
                timeout=30
            )
            
            if response.status_code == 200 or response.status_code == 201:
                return {
                    'success': True,
                    'transaction_id': reference,
                    'status': 'pending',
                    'message': f'Payment request sent to {phone_number}. Please check your phone.',
                    'payment_method': 'Airtel Money'
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment initiation failed: {response.text}'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Payment error: {str(e)}'
            }
    
    def check_payment_status(self, transaction_id):
        """Check payment status"""
        token = self.get_access_token()
        if not token:
            return {'status': 'unknown', 'message': 'Cannot verify payment'}
        
        headers = {
            'Authorization': f'Bearer {token}',
            'X-Country': 'UG',
            'X-Currency': 'UGX'
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/standard/v1/payments/{transaction_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                return {
                    'status': status.lower(),
                    'message': f'Payment {status}',
                    'data': data
                }
            return {'status': 'unknown', 'message': 'Could not verify payment'}
        except Exception as e:
            return {'status': 'unknown', 'message': str(e)}


class MockPaymentGateway:
    """Mock payment gateway for testing"""
    
    @staticmethod
    def initiate_payment(phone_number, amount, reference, user_id):
        return {
            'success': True,
            'transaction_id': f"MOCK-{reference}",
            'status': 'pending',
            'message': f'Test payment initiated. In production, this would send a USSD popup to {phone_number}',
            'payment_method': 'Test Mode'
        }
    
    @staticmethod
    def check_payment_status(transaction_id):
        return {
            'status': 'successful',
            'message': 'Payment successful (test mode)'
        }


# Select gateway based on environment
def get_payment_gateway(provider='mtn'):
    """Get the appropriate payment gateway"""
    
    # For development/testing, use mock gateway
    if settings.DEBUG:
        return MockPaymentGateway()
    
    # For production, use real gateways
    if provider == 'mtn':
        return MTNMoneyGateway()
    elif provider == 'airtel':
        return AirtelMoneyGateway()
    else:
        return MockPaymentGateway()
    
    import requests
import json
import hmac
import hashlib
from decimal import Decimal
from django.conf import settings
from .ip_whitelist import IPWhitelistMiddleware


class SecurePaymentGateway:
    """Base class with security features"""
    
    def validate_ip(self, request_ip):
        """Validate that request comes from whitelisted IP"""
        whitelist_middleware = IPWhitelistMiddleware(None)
        return whitelist_middleware.is_ip_whitelisted(request_ip, self.service_name)
    
    def verify_signature(self, data, signature, secret_key):
        """Verify webhook signature"""
        expected_signature = hmac.new(
            secret_key.encode(),
            json.dumps(data, sort_keys=True).encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)
    
    def sanitize_phone_number(self, phone_number):
        """Sanitize phone number for security"""
        import re
        # Remove non-digit characters
        phone = re.sub(r'\D', '', phone_number)
        # Ensure it starts with 256
        if phone.startswith('0'):
            phone = '256' + phone[1:]
        elif not phone.startswith('256'):
            phone = '256' + phone
        return phone


class MTNMoneyGateway(SecurePaymentGateway):
    """MTN Mobile Money Payment Gateway Integration with IP Whitelisting"""
    
    def __init__(self):
        self.service_name = 'mtn'
        self.api_url = settings.MTN_API_URL
        self.api_key = settings.MTN_API_KEY
        self.api_secret = settings.MTN_API_SECRET
        self.callback_url = settings.MTN_CALLBACK_URL
    
    def initiate_payment(self, phone_number, amount, reference, user_id, request_ip=None):
        """Initiate MTN Mobile Money payment with IP validation"""
        
        # Validate IP if provided
        if request_ip and not self.validate_ip(request_ip):
            return {
                'success': False,
                'message': 'Access denied from this IP address',
                'error_code': 'IP_BLOCKED'
            }
        
        # Sanitize phone number
        phone_number = self.sanitize_phone_number(phone_number)
        
        # Get access token
        token = self.get_access_token()
        if not token:
            return {
                'success': False,
                'message': 'Could not authenticate with MTN. Please try again.',
                'error_code': 'AUTH_FAILED'
            }
        
        # Prepare payment data
        payment_data = {
            'amount': str(amount),
            'currency': 'UGX',
            'externalId': reference,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': phone_number
            },
            'payerMessage': f'Payment for service request {reference}',
            'payeeNote': f'Buildimity payment - {reference}'
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'X-Reference-Id': str(uuid.uuid4()),
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/v1_0/collection/v1_0/requesttopay",
                headers=headers,
                json=payment_data,
                timeout=30
            )
            
            if response.status_code == 202:
                return {
                    'success': True,
                    'transaction_id': payment_data['externalId'],
                    'status': 'pending',
                    'message': f'Payment request sent to {phone_number}. Please check your phone.',
                    'payment_method': 'MTN Mobile Money'
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment initiation failed: {response.text}',
                    'error_code': 'API_ERROR'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Payment error: {str(e)}',
                'error_code': 'CONNECTION_ERROR'
            }
    
    def get_access_token(self):
        """Get OAuth access token from MTN with retry logic"""
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                auth_string = f"{self.api_key}:{self.api_secret}"
                encoded_auth = base64.b64encode(auth_string.encode()).decode()
                
                headers = {
                    'Authorization': f'Basic {encoded_auth}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f"{self.api_url}/v1_0/apiuser/{self.api_key}/apikey",
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json().get('access_token')
                
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                continue
        
        return None


class AirtelMoneyGateway(SecurePaymentGateway):
    """Airtel Money Payment Gateway Integration with IP Whitelisting"""
    
    def __init__(self):
        self.service_name = 'airtel'
        self.api_url = settings.AIRTEL_API_URL
        self.client_id = settings.AIRTEL_CLIENT_ID
        self.client_secret = settings.AIRTEL_CLIENT_SECRET
        self.callback_url = settings.AIRTEL_CALLBACK_URL
    
    def initiate_payment(self, phone_number, amount, reference, user_id, request_ip=None):
        """Initiate Airtel Money payment with IP validation"""
        
        # Validate IP if provided
        if request_ip and not self.validate_ip(request_ip):
            return {
                'success': False,
                'message': 'Access denied from this IP address',
                'error_code': 'IP_BLOCKED'
            }
        
        # Sanitize phone number
        phone_number = self.sanitize_phone_number(phone_number)
        
        # Get access token
        token = self.get_access_token()
        if not token:
            return {
                'success': False,
                'message': 'Could not authenticate with Airtel. Please try again.',
                'error_code': 'AUTH_FAILED'
            }
        
        payment_data = {
            'reference': reference,
            'subscriber': {
                'country': 'UG',
                'currency': 'UGX',
                'msisdn': phone_number
            },
            'transaction': {
                'amount': str(amount),
                'country': 'UG',
                'currency': 'UGX',
                'id': reference
            },
            'requestedAmount': str(amount),
            'country': 'UG',
            'currency': 'UGX'
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Country': 'UG',
            'X-Currency': 'UGX'
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/standard/v1/payments/",
                headers=headers,
                json=payment_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'transaction_id': reference,
                    'status': 'pending',
                    'message': f'Payment request sent to {phone_number}. Please check your phone.',
                    'payment_method': 'Airtel Money'
                }
            else:
                return {
                    'success': False,
                    'message': f'Payment initiation failed: {response.text}',
                    'error_code': 'API_ERROR'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Payment error: {str(e)}',
                'error_code': 'CONNECTION_ERROR'
            }