import importlib
import inspect
import os
import sys
from djangoautoconf import DjangoAutoConf
from djangoautoconf.auto_conf_utils import get_module_path, is_at_least_one_sub_filesystem_item_exists
from libtool.short_decorator.ignore_exception import ignore_exc_with_result

__author__ = 'weijia'
from django.conf.urls import include, url
from django.utils.importlib import import_module


class EasyList(object):
    def __init__(self, original_list):
        super(EasyList, self).__init__()
        self.list = original_list

    def append_list_to_head(self, list_to_head):
        for item in list_to_head:
            self.list.insert(0, item)

    def append(self, item):
        self.list.insert(0, item)


def get_custom_root_url_pattern_container():
    from django.conf import settings
    from django.utils.importlib import import_module

    root_url = import_module(settings.ROOT_URLCONF)
    root_url_pattern_list = root_url.default_app_url_patterns
    return EasyList(root_url_pattern_list)


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
    (get_custom_root_url_pattern_container()).append_list_to_head(url_pattern_list)


def add_default_root_url(default_url_root_path):
    frame = inspect.getouterframes(inspect.currentframe())
    urls_module = include(frame[1][0].f_locals["__name__"])
    add_url_pattern(default_url_root_path, urls_module)


def include_urls():
    from django.conf import settings
    from django.utils.importlib import import_module

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's urls module.
        try:
            urls_module = '%s.urls' % app
            import_module(urls_module)
        except ImportError, e:
            if str(e) != 'No module named urls':
                import traceback
                traceback.print_exc()

    sys.path.append(settings.DJANGO_AUTO_CONF_LOCAL_DIR)
    all_local_url_patterns = []
    local_urls_full_path = os.path.join(settings.DJANGO_AUTO_CONF_LOCAL_DIR, "local_urls")
    if os.path.exists(local_urls_full_path) and os.path.isdir(local_urls_full_path):
        for url_module_name in DjangoAutoConf.enum_modules(local_urls_full_path):
            # m = __import__("local_urls.%s" % url_module_name)
            m = importlib.import_module("local_urls.%s" % url_module_name)
            # m = importlib.import_module("%s.%s" % (module_path, self.module_of_attribute))
            urlpatterns = getattr(m, "urlpatterns")
            for p in urlpatterns:
                all_local_url_patterns.append(p)
    sys.path.remove(settings.DJANGO_AUTO_CONF_LOCAL_DIR)
    add_to_root_url_pattern(all_local_url_patterns)


def add_app_urls_no_exception(app):
    try:
        if not ("." in app):
            importlib.import_module("%s.urls" % app)
            add_url_pattern("^%s/" % app, include('%s.urls' % app))
    except ImportError:
        print "Import %s.urls failed (maybe %s.urls does not exists)." % (app, app)
    except Exception, e:
        import traceback
        traceback.print_exc()
        pass


def include_default_urls():
    for app in enum_apps():
        mod = import_module(app)
        # Attempt to import the app's admin module.
        if is_at_least_one_sub_filesystem_item_exists(get_module_path(mod), ["urls.py", "default_settings.py"]):
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
    #Include default urls first so the root url patterns will not take over the default urls.
    include_default_urls()
    include_urls()


