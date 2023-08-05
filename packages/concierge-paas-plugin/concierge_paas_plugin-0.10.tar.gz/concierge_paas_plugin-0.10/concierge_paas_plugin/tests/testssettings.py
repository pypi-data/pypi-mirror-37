from concierge_paas_plugin.settings import *

SECRET_KEY = "test-key"

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'concierge_paas_plugin_test.db',
        }
    }