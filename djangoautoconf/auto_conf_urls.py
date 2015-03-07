import inspect
from djangoautoconf.auto_conf_utils import get_module_path, is_at_least_one_sub_filesystem_item_exists
from libtool.short_decorator.ignore_exception import ignore_exc_with_result

__author__ = 'weijia'
from django.conf.urls import patterns, include, url


def get_custom_root_url_pattern_container():
    from django.conf import settings
    from django.utils.importlib import import_module

    root_url = import_module(settings.ROOT_URLCONF)
    root_url_pattern_list = root_url.default_app_url_patterns
    return root_url_pattern_list


def add_url_pattern(default_url_root_path, urls_module):
    """
    default_url_root_path: target URL to be matched
    urls_module:
                include('provider.oauth2.urls') or
                include(admin.site.urls) or
                RedirectView.as_view(url='/resource_bookmarks') etc.
    """
    (get_custom_root_url_pattern_container()).append(url(default_url_root_path, urls_module))


def add_to_root_url_pattern(url_pattern_list):
    (get_custom_root_url_pattern_container()).extend(url_pattern_list)


def add_default_root_url(default_url_root_path):
    frame = inspect.getouterframes(inspect.currentframe())
    urls_module = include(frame[1][0].f_locals["__name__"])
    add_url_pattern(default_url_root_path, urls_module)


def include_urls():
    from django.conf import settings
    from django.utils.importlib import import_module

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            urls_module = '%s.urls' % app
            import_module(urls_module)
        except ImportError, e:
            if str(e) != 'No module named urls':
                import traceback
                traceback.print_exc()


def add_app_urls_no_exception(app):
    try:
        add_url_pattern("^%s/" % app, include('%s.urls' % app))
    except:
        pass


def include_default_urls():
    from django.utils.importlib import import_module

    for app in enum_apps():
        mod = import_module(app)
        # Attempt to import the app's admin module.
        if is_at_least_one_sub_filesystem_item_exists(get_module_path(mod), ["default_settings.py"]):
            add_app_urls_no_exception(app)


def enum_apps():
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        yield app


def exc_wrapper_for_url_pattern(func):
    @ignore_exc_with_result([], ImportError)
    def wrapped_func():
        return func()

    return wrapped_func


def autodiscover():
    """
    Auto-discover INSTALLED_APPS urls.py modules and fail silently when
    not present. This forces an import on them to register any urls jobs they
    may want.
    """
    include_urls()
    include_default_urls()


