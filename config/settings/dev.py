from .base import *
from pathlib import Path
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY', 'default_secret_key')

DEBUG = config('DEBUG', True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS += [

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

