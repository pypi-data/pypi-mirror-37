from .settings import *

SECRET_KEY = "dev-key"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev_db.db',
    }
}