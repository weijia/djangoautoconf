import importlib
import inspect
import os
import sys
import traceback
from djangoautoconf.auto_conf_utils import get_module_path, is_at_least_one_sub_filesystem_item_exists
from ufs_tools.short_decorator.ignore_exception import ignore_exc_with_result
from djangoautoconf.auto_conf_utils import enum_modules
from django.conf.urls import include, url
from importlib import import_module

try:
    import simplemenu
    from simplemenu.models import MenuItem, Menu
except:
    pass


class EasyList(object):
    def __init__(self, original_list):
        super(EasyList, self).__init__()
        self.list = original_list

    def append_list_to_head(self, list_to_head):
        for item in list_to_head:
            if item not in self.list:
                self.list.insert(0, item)

    def insert_to_head(self, item):
        if item not in self.list:
            self.list.insert(0, item)


def get_custom_root_url_pattern_container():
    from django.conf import settings
    # from django.utils.importlib import import_module

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
    (get_custom_root_url_pattern_container()).insert_to_head(url(default_url_root_path, urls_module))


def add_to_root_url_pattern(url_pattern_list):
    (get_custom_root_url_pattern_container()).append_list_to_head(url_pattern_list)
    # for item in url_pattern_list:
    #     simplemenu.register(
    #         item._regex,
    #     )


def add_default_root_url(default_url_root_path):
    frame = inspect.getouterframes(inspect.currentframe())
    urls_module = include(frame[1][0].f_locals["__name__"])
    add_url_pattern(default_url_root_path, urls_module)


def include_urls():
    from django.conf import settings
    # from django.utils.importlib import import_module

    create_simple_menu("admin")

    for app in enum_app_names():
        mod = import_module(app)
        # Attempt to add app's urls.py automatically to root
        if is_at_least_one_sub_filesystem_item_exists(get_module_path(mod), ["urls.py", "default_settings.py"]):
            add_app_urls_no_exception(app)
        # Attempt to import the app's urls module.
        try:
            import_app_urls(app)
        except ImportError as e:
            if not ('No module named' in str(e) and 'url' in str(e)):
                # import traceback
                traceback.print_exc()

    local_urls_full_path = os.path.join(settings.DJANGO_AUTO_CONF_LOCAL_DIR, "local_urls")
    if os.path.exists(local_urls_full_path) and os.path.isdir(local_urls_full_path):
        add_urlpatterns_in_file(local_urls_full_path)


def import_app_urls(app):
    urls_module = '%s.urls' % app
    return import_module(urls_module)


def add_urlpatterns_in_file(local_urls_full_path):
    sys.path.append(local_urls_full_path)
    all_local_url_patterns = []
    for url_module_name in enum_modules(local_urls_full_path):
        # m = __import__("local_urls.%s" % url_module_name)
        m = importlib.import_module("%s" % url_module_name)
        # m = importlib.import_module("%s.%s" % (module_path, self.module_of_attribute))
        try:
            urlpatterns = getattr(m, "urlpatterns")
            for p in urlpatterns:
                all_local_url_patterns.append(p)
            add_to_root_url_pattern(all_local_url_patterns)
        except AttributeError:
            pass
    sys.path.remove(local_urls_full_path)


def has_api_url(app_module):
    # return True
    for pattern in app_module.urlpatterns:
        if (hasattr(pattern, "_regex") and pattern._regex is not None) and ('^api_domain_needed_signature/' in pattern._regex):
            return True
    return False


def add_app_urls_no_exception(app):
    try:
        if not ("." in app):
            app_module = import_app_urls(app)
            if hasattr(app_module, "urlpatterns"):
                if has_api_url(app_module):
                    include_param = include('%s.urls' % app,
                                            namespace=app,  # Used by tastypie swagger API
                                            )
                else:
                    include_param = include('%s.urls' % app)
                add_url_pattern("^%s/" % app, include_param)
                create_simple_menu(app)
    except ImportError:
        print("Import %s.urls failed (maybe %s.urls does not exists)." % (app, app))
    except Exception as e:
        # import traceback
        traceback.print_exc()
        pass


def create_simple_menu(app):
    try:
        menu, is_created = Menu.objects.get_or_create(name=app)
        item, is_created = MenuItem.objects.get_or_create(name=app, menu=menu, urlstr="/%s/" % app)
        if app in ["admin", "simplemenu"] and not item.is_valid:
            item.is_valid = True
            item.save()
    except Exception as e:
        # import traceback
        pass


def enum_app_names():
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
    # Include default urls first so the root url patterns will not take over the default urls.
    # include_default_urls()
    include_urls()
