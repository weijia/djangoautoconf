import inspect

__author__ = 'weijia'
from django.conf.urls import patterns, include, url


def add_default_root_url(default_url_root_path):
    from django.conf import settings
    from django.utils.importlib import import_module
    import os
    root_url = import_module(settings.ROOT_URLCONF)
    frame = inspect.getouterframes(inspect.currentframe())
    include_url = url(default_url_root_path, include(frame[1][0].f_locals["__name__"]))
    root_url.default_app_url_patterns.append(include_url)


def autodiscover():
    """
    Auto-discover INSTALLED_APPS cron.py modules and fail silently when
    not present. This forces an import on them to register any cron jobs they
    may want.
    """
    from django.conf import settings
    from django.utils.importlib import import_module
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            import_module('%s.urls' % app)
        except:
            pass
