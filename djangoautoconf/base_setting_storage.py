import importlib
import logging
import sys
from sys import modules as sys_modules

from ufs_tools.tuple_tools import remove_duplicated_keep_order

log = logging.getLogger(__name__)


# class SettingStorageInf(object):
#     pass

class BaseSettingsHolder(object):
    # MYSQL_DATABASE_NAME = "test"
    AUTHENTICATION_BACKENDS = []
    # WSGI_APPLICATION = 'default_django_15_and_below.wsgi.application'
    DATABASE_ROUTERS = []
    TEMPLATE_CONTEXT_PROCESSORS = []
    ROOT_URLCONF = "djangoautoconf.urls"
    INSTALLED_APPS = ["django.contrib.sites"]


class ObjectSettingStorage(object):
    base_settings = BaseSettingsHolder()

    def __init__(self, root_dir):
        super(ObjectSettingStorage, self).__init__()
        # self.unwanted_attr_names = ["TEMPLATE_"]
        self.unwanted_attr_names = ['WSGI_APPLICATION']
        self.root_dir = root_dir

    def import_based_on_base_settings(self, module_import_path):
        # ######
        # Inject attributes to builtin and import all other modules
        # Ref: http://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function
        self.__init_builtin()
        self.__inject_attr()
        try:
            new_base_settings = importlib.import_module(module_import_path)
        except:
            print "Import module error:", module_import_path
            raise
        self.__remove_lower_case_attributes(new_base_settings)
        self.update_base_settings(new_base_settings)
        del sys_modules[module_import_path]

    def __init_builtin(self):
        try:
            self.__dict__['builtin'] = sys.modules['__builtin__'].__dict__
        except KeyError:
            self.__dict__['builtin'] = sys.modules['builtins'].__dict__

    def __inject_attr(self):
        self.builtin["PROJECT_ROOT"] = self.root_dir
        for attr in dir(self.base_settings):
            if attr != attr.upper():
                continue
            value = getattr(self.base_settings, attr)
            if hasattr(self.builtin, attr):
                raise "Attribute already exists"
            self.builtin[attr] = value

    def update_base_settings(self, new_base_settings):
        for attr in dir(new_base_settings):
            if attr != attr.upper():
                continue
            value = getattr(new_base_settings, attr)
            setattr(self.base_settings, attr, value)
        logging.debug(self.base_settings.INSTALLED_APPS)

    @staticmethod
    def __remove_lower_case_attributes(new_base_settings):
        for attr in dir(new_base_settings):
            if attr == attr.upper():
                continue
            delattr(new_base_settings, attr)

    def remove_empty_list(self):
        for attr in dir(self.base_settings):
            value = getattr(self.base_settings, attr)
            if (type(value) is list) and len(value) == 0:
                delattr(self.base_settings, attr)

    def refine_attributes(self):
        for attr in dir(self.base_settings):
            if attr in self.unwanted_attr_names:
                delattr(self.base_settings, attr)
                continue
            if attr != attr.upper():
                # Do not process lower case var
                continue
            value = getattr(self.base_settings, attr)
            if (type(value) is list) and len(value) == 0:
                delattr(self.base_settings, attr)
            if type(value) is tuple:
                setattr(self.base_settings, attr, remove_duplicated_keep_order(value))

    def set_attr(self, attr, value):
        setattr(self.base_settings, attr, value)

    def set_installed_apps(self, installed_app_list):
        setattr(self.base_settings, "INSTALLED_APPS", tuple(installed_app_list))

    def get_installed_apps(self):
        return list(getattr(self.base_settings, "INSTALLED_APPS"))

    def add_secret_key(self, secret_key):
        setattr(self.base_settings, "SECRET_KEY", secret_key)

    # noinspection PyMethodMayBeStatic
    def get_settings(self):
        return self.base_settings

