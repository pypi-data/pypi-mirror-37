import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concierge_paas_plugin.settings')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'oidc_provider',
    'rest_framework',
    'rest_framework.authtoken',
    'concierge_paas_plugin',
    'user_sessions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = []
DEBUG =True

SECRET_KEY = os.getenv('SECRET_KEY')

ROOT_URLCONF = 'concierge_paas_plugin.urls'

USE_TZ = True