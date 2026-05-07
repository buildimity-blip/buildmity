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
    "10.0.2.2",
    "192.168.1.%",
    "*",
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
    'corsheaders',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    'users',
    'jobs',
]

# 🔁 MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.DynamicSiteMiddleware',
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

# 💾 DATABASE
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

# ========== ALLAUTH SETTINGS ==========
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  # Auto-generate username from email
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

# Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
            'key': ''
        }
    }
}

# Redirects
LOGIN_REDIRECT_URL = '/redirect-after-login/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

# 📁 STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 📷 MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 💰 FLUTTERWAVE CONFIGURATION
FLUTTERWAVE_PUBLIC_KEY = os.environ.get('FLUTTERWAVE_PUBLIC_KEY', '')
FLUTTERWAVE_SECRET_KEY = os.environ.get('FLUTTERWAVE_SECRET_KEY', '')
FLUTTERWAVE_ENCRYPTION_KEY = os.environ.get('FLUTTERWAVE_ENCRYPTION_KEY', '')
FLUTTERWAVE_ENVIRONMENT = os.environ.get('FLUTTERWAVE_ENVIRONMENT', 'sandbox')
FLUTTERWAVE_CALLBACK_URL = os.environ.get('FLUTTERWAVE_CALLBACK_URL', '')

# ========== PESAPAL CONFIGURATION ==========
PESAPAL_CONSUMER_KEY = os.environ.get('PESAPAL_CONSUMER_KEY', '')
PESAPAL_CONSUMER_SECRET = os.environ.get('PESAPAL_CONSUMER_SECRET', '')
PESAPAL_ENVIRONMENT = os.environ.get('PESAPAL_ENVIRONMENT', 'sandbox')  # sandbox or live
PESAPAL_CALLBACK_URL = os.environ.get('PESAPAL_CALLBACK_URL', '/payment/callback/')
PESAPAL_IPN_URL = os.environ.get('PESAPAL_IPN_URL', '/payment/ipn/')

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

# 🗺️ GOOGLE MAPS
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'AIzaSyD5MMXNAyFgmaGNgMMC_Q81dbKXtAnsLPM')

# 🌐 SITES FRAMEWORK
if DEBUG:
    SITE_URL = 'http://127.0.0.1:8000'
else:
    SITE_URL = 'https://buildimity.com'
