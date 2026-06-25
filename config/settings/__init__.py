import os

env = os.getenv('DJNAGO_ENV', 'dev')

if env == 'dev':
    from .dev import *

if env == 'prod':
    from .prod import *