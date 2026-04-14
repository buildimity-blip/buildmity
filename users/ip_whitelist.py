import os
from decouple import config

# IP Whitelist Configuration
IP_WHITELIST_CONFIG = {
    'mtn': {
        'sandbox': [
            '52.20.112.96',      # MTN Sandbox API Server
            '54.221.171.118',    # MTN Sandbox API Server
            '34.228.210.72',     # MTN Sandbox API Server
        ],
        'production': [
            '52.20.112.96',      # MTN Production API Server
            '54.221.171.118',    # MTN Production API Server
            '34.228.210.72',     # MTN Production API Server
        ]
    },
    'airtel': {
        'sandbox': [
            '52.20.112.96',      # Airtel Sandbox
            '54.221.171.118',    # Airtel Sandbox
        ],
        'production': [
            '52.20.112.96',      # Airtel Production
            '54.221.171.118',    # Airtel Production
        ]
    },
    'your_servers': {
        'development': [
            '127.0.0.1',
            'localhost',
        ],
        'production': [
            # Add your server IPs here
        ]
    }
}

# Get IPs from environment variables
MTN_ALLOWED_IPS = config('MTN_ALLOWED_IPS', default='').split(',')
AIRTEL_ALLOWED_IPS = config('AIRTEL_ALLOWED_IPS', default='').split(',')
CALLBACK_ALLOWED_IPS = config('CALLBACK_ALLOWED_IPS', default='').split(',')


class IPWhitelistMiddleware:
    """Middleware to check if request IP is whitelisted"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        
        # Skip IP check for admin and debug
        if request.path.startswith('/admin/') or request.path.startswith('/debug/'):
            return self.get_response(request)
        
        # For payment callbacks, check whitelist
        if request.path in ['/api/mtn-callback/', '/api/airtel-callback/']:
            if not self.is_ip_whitelisted(client_ip, 'callback'):
                from django.http import JsonResponse
                return JsonResponse({
                    'error': 'Access Denied',
                    'message': f'IP {client_ip} is not whitelisted',
                    'status': 403
                }, status=403)
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_whitelisted(self, ip, service='callback'):
        from django.conf import settings
        
        if service == 'callback':
            allowed_ips = CALLBACK_ALLOWED_IPS
        elif service == 'mtn':
            allowed_ips = MTN_ALLOWED_IPS
        elif service == 'airtel':
            allowed_ips = AIRTEL_ALLOWED_IPS
        else:
            allowed_ips = []
        
        if settings.DEBUG:
            allowed_ips.extend(IP_WHITELIST_CONFIG['your_servers']['development'])
        else:
            allowed_ips.extend(IP_WHITELIST_CONFIG['your_servers']['production'])
        
        return ip in allowed_ips