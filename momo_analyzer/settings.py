from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secret key hardcoded as requested (NOT recommended for production)
SECRET_KEY = 'z1b7k8wd-eexbza7s&$_r4qwgkel5nw&o1&)pys!)bhc9d$$m('

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    os.getenv('RENDER_EXTERNAL_HOSTNAME', 'airtime-checker.onrender.com')
]

INSTALLED_APPS = [
    'analyzer',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'momo_analyzer.wsgi.application'

# Database configuration
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    # Production settings for Render
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'momo_analyzer'),
            'USER': os.getenv('POSTGRES_USER', 'momo_analyzer_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }
else:
    # Local development settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Static files configuration for production
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = []
