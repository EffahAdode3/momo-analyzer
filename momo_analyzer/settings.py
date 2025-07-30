from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secret key hardcoded as requested (NOT recommended for production)
SECRET_KEY = 'z1b7k8wd-eexbza7s&$_r4qwgkel5nw&o1&)pys!)bhc9d$$m('

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    os.getenv('RENDER_EXTERNAL_HOSTNAME', 'airtime-checker.onrender.com')
]

INSTALLED_APPS = [
    'analyzer',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'momo_analyzer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'momo_analyzer.wsgi.application'

# No database configuration needed
DATABASES = {}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Static files configuration for production
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = []
