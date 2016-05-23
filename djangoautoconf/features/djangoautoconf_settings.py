INSTALLED_APPS = (
    'bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'south',  # Do not work in SAE
    # 'mptt',
    # 'treenav',
    # 'background_task',
    # 'django_cron',  # Do not work in SAE
    'jquery_ui',
    # 'provider',
    # 'provider.oauth2',
    'guardian',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
)

AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',
                            'guardian.backends.ObjectPermissionBackend')

ANONYMOUS_USER_ID = -1

SITE_ID = 1

ROOT_URLCONF = "djangoautoconf.urls"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

DATABASE_ROUTERS = []