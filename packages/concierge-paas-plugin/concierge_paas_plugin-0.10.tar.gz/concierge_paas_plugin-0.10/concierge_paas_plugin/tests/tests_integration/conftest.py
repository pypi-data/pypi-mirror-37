import os
import django
from django.conf import settings

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concierge_paas_plugin.tests.testssettings')


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = True

    settings.PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'concierge_paas_plugin_test.db',
        }
    }

    # If you have any test specific settings, you can declare them here,
    # e.g.
    # settings.PASSWORD_HASHERS = (
    #     'django.contrib.auth.hashers.MD5PasswordHasher',
    # )
    django.setup()
    # Note: In Django =< 1.6 you'll need to run this instead
    # settings.configure()
