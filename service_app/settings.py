import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECURITY
SECRET_KEY = 'dev-secret-key'
DEBUG = True

# IP Whitelisting for Payment Gateways
MTN_ALLOWED_IPS = os.environ.get('MTN_ALLOWED_IPS', '').split(',')
AIRTEL_ALLOWED_IPS = os.environ.get('AIRTEL_ALLOWED_IPS', '').split(',')
CALLBACK_ALLOWED_IPS = os.environ.get('CALLBACK_ALLOWED_IPS', '').split(',')

# Add IP Whitelist Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'users.ip_whitelist.IPWhitelistMiddleware',  # Add this
    # ... other middleware
]
ALLOWED_HOSTS = [
    "buildimity.com",
    "www.buildimity.com",
    ".railway.app",   # VERY IMPORTANT for Railway
    "localhost",
    "127.0.0.1",
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

    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'users',
    'jobs',
]


# 🔁 MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
]


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

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,
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


# 📷 MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 🔄 LOGIN REDIRECTS

LOGOUT_REDIRECT_URL = '/login/'
LOGIN_REDIRECT_URL = '/redirect-after-login/'

# 📧 ALLAUTH SETTINGS
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}


# 🔌 DRF (optional for later API use)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# Sites Framework - for sitemap domain
SITE_ID = 1

# For development, you can force the domain
if DEBUG:
    SITE_URL = 'http://127.0.0.1:8000'
else:
    SITE_URL = 'https://buildimity.com'