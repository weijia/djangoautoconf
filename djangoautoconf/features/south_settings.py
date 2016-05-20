import django

if django.__version__ < "1.6.0":
    INSTALLED_APPS += (
        'south',
    )
