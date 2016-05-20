
# MYSQL_DATABASE_NAME = "test"
AUTHENTICATION_BACKENDS = []
# WSGI_APPLICATION = 'default_django_15_and_below.wsgi.application'
DATABASE_ROUTERS = []
TEMPLATE_CONTEXT_PROCESSORS = []
ROOT_URLCONF = "djangoautoconf.urls"
INSTALLED_APPS = list(INSTALLED_APPS) + ["django.contrib.sites"]
