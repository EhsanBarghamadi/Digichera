from .base import *
from pathlib import Path
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY', 'default_secret_key')

DEBUG = config('DEBUG', True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS += [
    # Local Apps
    'page',
    'core',
    'user',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

AUTH_USER_MODEL = 'user.CustomUser'

