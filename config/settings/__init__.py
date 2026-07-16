import os

env = os.getenv('DJANGO_ENV', 'dev')

if env == 'dev':
    from .dev import *

if env == 'prod':
    from .prod import *