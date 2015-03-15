"""
Django settings for fitting project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import json

env = {}
# noinspection PyBroadException
try:
    with open('env.json', 'r') as f:
        env = json.load(f)
except Exception:
    pass  # If the env.json not existing, we do nothing

SECRET_KEY = 'mk&81(7*-#kzj_ctc0eqt(go4a@d&t9aook$z3@b@a5r5hqe7g'

# dev staging prod
if env.get('environment', 'dev') != "dev":
    DEBUG = False
    TEMPLATE_DEBUG = False
else:
    DEBUG = True
    TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'ft_accounts',
    'ft_fitting',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fitting.urls'

WSGI_APPLICATION = 'fitting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'config/mysql.conf'),
        }
    },
}

if env.get('environment', 'dev') != 'prod':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.59.103',
        'PORT': 3306,
        'NAME': 'fitting',
        'USER': 'fitting',
        'PASSWORD': 'Fitting123',
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'publish/static')

# Media files path
MEDIA_ROOT = '/var/media/fitting/'
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

# Authentication backend
AUTHENTICATION_BACKENDS = (
    'ft_accounts.auth_backend.AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)