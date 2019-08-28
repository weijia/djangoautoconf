import importlib
import logging
import os
import sys
from sys import modules as sys_modules

import django
from ufs_tools import get_folder

from ufs_tools.tuple_tools import remove_duplicated_keep_order

log = logging.getLogger(__name__)


# class SettingStorageInf(object):
#     pass

class BaseSettingsHolder(object):
    # MYSQL_DATABASE_NAME = "test"
    # WSGI_APPLICATION = 'default_django_15_and_below.wsgi.application'
    AUTHENTICATION_BACKENDS = []
    TEMPLATE_CONTEXT_PROCESSORS = []
    ROOT_URLCONF = "djangoautoconf.urls"
    INSTALLED_APPS = ["django.contrib.sites",
                      ]
    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/media/"

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
    STATIC_URL = "/static/"
    TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            "django.contrib.auth.context_processors.auth",
                            'django.contrib.messages.context_processors.messages',
                        ]
                    }
                },
            ]
    DEBUG = True


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
        except Exception as e:
            print("Import module error:", module_import_path)
            raise e
        self.__remove_lower_case_attributes(new_base_settings)
        self.update_base_settings(new_base_settings)
        del sys_modules[module_import_path]

    def eval_content(self, module_file_content):
        # ######
        # Inject attributes to builtin and import all other modules
        # Ref: http://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function
        self.__init_builtin()
        self.__inject_attr()
        ctx = {}
        exec(module_file_content, globals(), ctx)
        self.__remove_lower_case_attributes(ctx)
        self.update_base_settings(ctx)
        self.update_base_settings(ctx)

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
            # if attr.startswith("__"):
            #     continue
            # if attr in ["__class__", "__cmp__", "__contains__", "clear", "copy"]:
            #     continue
            if attr == attr.upper():
                continue
            try:
                delattr(new_base_settings, attr)
            except:
                # print attr
                continue

    def remove_empty_list(self):
        for attr in dir(self.base_settings):
            value = getattr(self.base_settings, attr)
            if (type(value) is list) and len(value) == 0:
                delattr(self.base_settings, attr)

    def refine_attributes(self):
        self.refine_attributes_for_django18()
        for attr in dir(self.base_settings):
            if attr in self.unwanted_attr_names:
                delattr(self.base_settings, attr)
                continue
            if attr != attr.upper():
                # Do not process lower case var
                continue
            value = getattr(self.base_settings, attr)
            if (type(value) is list) and len(value) == 0:
                if hasattr(self.base_settings.__class__, attr):
                    delattr(self.base_settings.__class__, attr)
                else:
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

    def refine_attributes_for_django18(self):
        attr = "TEMPLATE_CONTEXT_PROCESSORS"
        target_attr = "TEMPLATES"
        if self.is_above_or_equal_to_django18() and (attr in dir(self.base_settings)):
            value = getattr(self.base_settings, attr)

            default_template_value = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'DIRS': [
                        self.root_dir
                    ],
                    'OPTIONS': {
                        'context_processors': [],
                    }
                },
            ]

            template_engines = getattr(self.base_settings, "TEMPLATES", default_template_value)

            # The original TEMPLATE setting must have one element if the TEMPLATE setting exists
            template_engine0 = template_engines[0]
            module_template_folder = os.path.join(get_folder(__file__), "templates")
            if 'DIRS' in template_engine0:
                template_engine0['DIRS'].append(module_template_folder)
            else:
                template_engine0['DIRS'] = [module_template_folder]

            template_options = template_engine0.get("OPTIONS", {'context_processors': []})

            template_options["context_processors"].extend(set(value))

            # delattr(self.base_settings, attr)
            setattr(self.base_settings, target_attr, template_engines)
            # del self.base_settings.TEMPLATE_CONTEXT_PROCESSORS
            for template_attr in ["TEMPLATE_STRING_IF_INVALID", "TEMPLATE_DIRS", "TEMPLATE_LOADERS",
                                  "TEMPLATE_DEBUG", attr]:
                if hasattr(self.base_settings, template_attr):
                    try:
                        delattr(self.base_settings.__class__, template_attr)
                    except:
                        pass
                    try:
                        delattr(self.base_settings, template_attr)
                    except:
                        pass

    # noinspection PyMethodMayBeStatic
    def is_above_or_equal_to_django18(self):
        return (django.VERSION[0] == 1) and (django.VERSION[1] >= 8)

    # noinspection PyMethodMayBeStatic
    def is_above_or_equal_to_django1_11(self):
        return not ((django.VERSION[0] == 1) and (django.VERSION[1] < 11))
