# Base setting file, content will be imported in DjangoAutoConf
# Default database name, can be override in extra_settings.settings
from .django_dev_server_auto_conf import DjangoDevServerAutoConf

MYSQL_DATABASE_NAME = "test"

AUTHENTICATION_BACKENDS = []

DATABASE_ROUTERS = []

MEDIA_URL = "/media/"

MEDIA_ROOT = "/media/"

f = DjangoDevServerAutoConf()
f.configure()

final_settings = f.django_auto_conf.setting_storage.get_settings()

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

for attr in dir(final_settings):
    vars()[attr] = getattr(final_settings, attr)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
