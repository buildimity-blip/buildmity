import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECURITY
SECRET_KEY = 'dev-secret-key'
DEBUG = True

ALLOWED_HOSTS = [
    "buildimity.com",
    "www.buildimity.com",
    ".railway.app",
    "localhost",
    "127.0.0.1",
    "10.0.2.2",           # Android emulator
    "192.168.1.%",        # Your local network
    "*",                  # Development only
]

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "https://buildmity-production.up.railway.app,https://buildimity.com,https://www.buildimity.com"
).split(",")

# 🔧 APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',  # ADDED
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    'users',
    'jobs',
]

# 🔁 MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ADDED AT TOP
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
<<<<<<< HEAD
    'users.middleware.DynamicSiteMiddleware',  # Dynamic site domain
=======
>>>>>>> a83b2e658e486bfae7938737abce081f71e39692
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://10.0.2.2:8000",
]
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = ['accept', 'accept-encoding', 'authorization', 'content-type', 'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with']

ROOT_URLCONF = 'service_app.urls'

# 🎨 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'service_app.wsgi.application'


import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:VuoenCfAicFsXMmRPiSGSmvMuTmnTHMP@interchange.proxy.rlwy.net:37163/railway',
        conn_max_age=600,
        ssl_require=False
    )
}

# 👤 CUSTOM USER
AUTH_USER_MODEL = 'users.User'
SITE_ID = 1

# 🔐 AUTH BACKENDS
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 📁 STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 📷 MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔄 LOGIN REDIRECTS
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_REDIRECT_URL = '/redirect-after-login/'

<<<<<<< HEAD
# Social Login - Google OAuth
=======
# Social Login
from decouple import config

>>>>>>> a83b2e658e486bfae7938737abce081f71e39692
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            'key': ''
        }
    }
}

ACCOUNT_EMAIL_VERIFICATION = 'none'
<<<<<<< HEAD
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# Flutterwave Configuration
FLUTTERWAVE_PUBLIC_KEY = config('FLUTTERWAVE_PUBLIC_KEY', default='')
FLUTTERWAVE_SECRET_KEY = config('FLUTTERWAVE_SECRET_KEY', default='')
FLUTTERWAVE_ENCRYPTION_KEY = config('FLUTTERWAVE_ENCRYPTION_KEY', default='')
FLUTTERWAVE_ENVIRONMENT = config('FLUTTERWAVE_ENVIRONMENT', default='sandbox')
FLUTTERWAVE_CALLBACK_URL = config('FLUTTERWAVE_CALLBACK_URL', default='')
# Add this to your settings.py (after your existing Flutterwave config)

# Dynamic callback URL based on domain
def get_flutterwave_callback_url(request):
    """Generate callback URL dynamically based on request domain"""
    domain = request.get_host()
    protocol = 'https' if request.is_secure() else 'http'
    return f"{protocol}://{domain}/payment/callback/"
=======
SOCIALACCOUNT_LOGIN_ON_GET = True
>>>>>>> a83b2e658e486bfae7938737abce081f71e39692

# 🔌 DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Sites Framework
if DEBUG:
    SITE_URL = 'http://127.0.0.1:8000'
else:
    SITE_URL = 'https://buildimity.com'
    # Google Maps API Key
GOOGLE_MAPS_API_KEY = 'AIzaSyD5MMXNAyFgmaGNgMMC_Q81dbKXtAnsLPM'
