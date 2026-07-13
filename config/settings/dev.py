from .base import *
from pathlib import Path
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY', 'default_secret_key')

DEBUG = config('DEBUG', True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS += [
    # Third-party Apps
    'localflavor',
    # Local Apps
    'page',
    'core',
    'user',
    'account',
    'store',
    'product',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

AUTH_USER_MODEL = 'user.CustomUser'

LOGIN_URL = 'user:login'
LOGIN_REDIRECT_URL = 'page:home'
LOGOUT_REDIRECT_URL = 'page:home'

LANGUAGE_CODE = 'fa-ir'

USE_I18N = True