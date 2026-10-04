"""
Django settings for the miscellany project.

Secrets and per-server values come from environment variables, loaded from
/home/misc/.env (by Gunicorn's EnvironmentFile on the server).
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Core

SECRET_KEY = os.environ['MISC_SECRET_KEY']

# Off unless MISC_DEBUG=1 is set (e.g. when running locally)
DEBUG = os.environ.get('MISC_DEBUG') == '1'

ALLOWED_HOSTS = [
    '134.122.29.200',
    '127.0.0.1',
    'localhost',
    'www.ericheep.com',
    'ericheep.com',
]


# HTTPS: Nginx handles TLS and tells Django via this header

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = ['https://ericheep.com', 'https://www.ericheep.com']
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# Start at one hour; raise to 31536000 (one year) once HTTPS has proven stable
SECURE_HSTS_SECONDS = 0 if DEBUG else 3600
# Share only the site's address (not the full page URL) with other sites.
# YouTube embeds refuse to play without it (error 153); Django's default
# 'same-origin' sends nothing to other sites.
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'


# Application definition

PROJECT_APPS = [
    'portfolio',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'miscellany.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'miscellany.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['MISC_DB_NAME'],
        'USER': os.environ['MISC_DB_USER'],
        'HOST': os.environ['MISC_DB_HOST'],
        'PASSWORD': os.environ['MISC_DB_PASSWORD'],
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static and media files (served by Nginx from www/)

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')


# Logging: send errors to Gunicorn's output (sudo journalctl -u gunicorn)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {'django': {'handlers': ['console'], 'level': 'WARNING'}},
}
