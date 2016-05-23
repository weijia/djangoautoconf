import django

if django.VERSION < "1.6.0":
    INSTALLED_APPS += (
        'south',
    )
