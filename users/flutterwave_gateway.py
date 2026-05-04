import requests
import json
import uuid
from decimal import Decimal
from django.conf import settings
from .flutterwave_config import FLUTTERWAVE_CONFIG


class FlutterwaveGateway:
    """Flutterwave Payment Gateway Integration"""
    
    def __init__(self):
        self.base_url = 'https://api.flutterwave.com/v3'
        self.public_key = FLUTTERWAVE_CONFIG['public_key']
        self.secret_key = FLUTTERWAVE_CONFIG['secret_key']
        self.encryption_key = FLUTTERWAVE_CONFIG['encryption_key']
        self.environment = FLUTTERWAVE_CONFIG['environment']
        
        # For sandbox, use test keys
        if self.environment == 'sandbox':
            self.base_url = 'https://api.flutterwave.com/v3'
    
    def get_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }
    
    def initialize_payment(self, transaction_id, amount, email, phone_number, name, payment_method='mobilemoney_uganda'):
        """Initialize payment with Flutterwave"""
        
        # Format phone number
        if phone_number.startswith('0'):
            phone_number = '256' + phone_number[1:]
        elif not phone_number.startswith('256'):
            phone_number = '256' + phone_number
        
        # Payment data
        payment_data = {
            'tx_ref': transaction_id,
            'amount': str(float(amount)),
            'currency': 'UGX',
            'redirect_url': FLUTTERWAVE_CONFIG['callback_url'],
            'customer': {
                'email': email,
                'phonenumber': phone_number,
                'name': name
            },
            'customizations': {
                'title': 'Buildimity Payment',
                'description': f'Payment for service request',
                'logo': 'https://buildimity.com/static/logo.png'
            },
            'payment_options': 'mobilemoney_uganda,card,ussd'
        }
        
        # Add payment method specific data
        if payment_method == 'mtn':
            payment_data['payment_plan'] = None
        elif payment_method == 'airtel':
            payment_data['payment_plan'] = None
        
        try:
            response = requests.post(
                f'{self.base_url}/payments',
                headers=self.get_headers(),
                json=payment_data,
                timeout=30
            )
            
            print(f"Flutterwave Response: {response.status_code} - {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return {
                        'success': True,
                        'transaction_id': transaction_id,
                        'payment_link': data['data']['link'],
                        'reference': data['data']['tx_ref'],
                        'status': 'pending',
                        'message': 'Payment initiated successfully'
                    }
                else:
                    return {
                        'success': False,
                        'message': data.get('message', 'Payment initiation failed')
                    }
            else:
                return {
                    'success': False,
                    'message': f'Payment initiation failed: {response.text}'
                }
        except Exception as e:
            print(f"Flutterwave Error: {str(e)}")
            return {
                'success': False,
                'message': f'Payment error: {str(e)}'
            }
    
    def verify_payment(self, transaction_id):
        """Verify payment status"""
        try:
            response = requests.get(
                f'{self.base_url}/transactions/{transaction_id}/verify',
                headers=self.get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    payment_data = data['data']
                    return {
                        'status': 'successful',
                        'amount': payment_data.get('amount'),
                        'currency': payment_data.get('currency'),
                        'transaction_id': payment_data.get('tx_ref'),
                        'message': 'Payment verified successfully'
                    }
                else:
                    return {
                        'status': 'failed',
                        'message': data.get('message', 'Payment verification failed')
                    }
            else:
                return {
                    'status': 'failed',
                    'message': f'Verification failed: {response.text}'
                }
        except Exception as e:
            return {
                'status': 'failed',
                'message': f'Verification error: {str(e)}'
            }