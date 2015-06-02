#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import logging
import os
import sys

from django.utils.crypto import get_random_string
import re

import base_settings
from auto_conf_utils import dump_attrs, is_at_least_one_sub_filesystem_item_exists
from libtool.folder_tool import ensure_dir


log = logging.getLogger(__name__)


class RootDirNotExist(Exception):
    pass


class LocalKeyFolderNotExist(Exception):
    pass


class DjangoAutoConf(object):
    def __init__(self, default_settings_import_str=None):
        self.default_settings_import_str = default_settings_import_str
        self.root_dir = None
        # Default keys is located at ../keys relative to universal_settings module?
        self.key_dir = None
        self.local_key_folder = None
        self.extra_settings = []
        self.project_path = None
        self.external_app_folder_name = "external_apps"
        self.local_key_folder_name = "local_keys"
        self.local_folder_name = "local"
        self.local_key_folder_relative_to_root = os.path.join(self.local_folder_name, self.local_key_folder_name)
        self.local_settings_relative_folder = "local/local_settings"
        self.external_apps_folder = None
        self.local_app_setting_folder = None
        self.external_settings_root_folder_name = "others"
        self.external_settings_folder_name = "external_settings"

    def set_default_settings(self, default_settings_import_str):
        self.default_settings_import_str = default_settings_import_str

    def set_root_dir(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.project_path = os.path.abspath(os.path.abspath(self.root_dir))
        self.local_key_folder = os.path.join(self.root_dir, self.local_key_folder_relative_to_root)
        self.local_app_setting_folder = os.path.join(self.root_dir, self.local_settings_relative_folder)

    def set_key_dir(self, key_dir):
        self.key_dir = key_dir
        self.local_key_folder = os.path.join(self.key_dir, self.local_key_folder_name)

    def set_local_key_folder(self, local_key_folder):
        self.local_key_folder = local_key_folder
        
    def get_folder_for_settings_in_external_apps_folder(self):
        external_settings_root_folder = os.path.join(self.get_external_apps_folder(),
            self.external_settings_root_folder_name)
        folder_for_external_apps_settings = os.path.join(external_settings_root_folder,
                                                         self.external_settings_folder_name)
        return folder_for_external_apps_settings
        
    @staticmethod
    def enum_modules(folder):
        for filename in os.listdir(folder):
            is_py = re.search('\.py$', filename)
            if is_py and (filename != "__init__.py"):
                yield filename.replace(".py", "")

    def add_extra_settings_from_folder(self, local_setting_dir=None):
        extra_setting_list = ["extra_settings.settings"]
        if local_setting_dir is None:
            local_setting_dir = self.local_app_setting_folder
        for module_name in self.enum_modules(local_setting_dir):
            extra_setting_list.append("local.local_settings.%s" % module_name)
        
        # Add external settings in external apps folder
        settings_folder_in_external_apps_folder = self.get_folder_for_settings_in_external_apps_folder()
        if os.path.exists(settings_folder_in_external_apps_folder):
            for module_name in self.enum_modules(settings_folder_in_external_apps_folder):
                extra_setting_list.append("%s.%s" % (self.external_settings_folder_name, module_name))
        self.add_extra_settings(extra_setting_list)

    def add_extra_settings(self, extra_setting_list):
        self.extra_settings.extend(extra_setting_list)

    def get_setting_module_list(self, features):
        ordered_import_list = [self.default_settings_import_str,
                               "djangoautoconf.sqlite_database"
                               # "djangoautoconf.mysql_database"
        ]
        ordered_import_list.extend(self.extra_settings)
        for feature in features:
            self.ordered_import_list.append("djangoautoconf.features." + feature)
        return ordered_import_list

    def configure(self, features=[]):
        self.check_params()

        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoautoconf.base_settings")
        os.environ["DJANGO_SETTINGS_MODULE"] = "djangoautoconf.base_settings"

        ordered_import_list = self.get_setting_module_list(features)

        for one_setting in ordered_import_list:
            self.import_based_on_base_settings(one_setting)

        self.add_secret_key()
        self.update_installed_apps_etc()

        dump_attrs(base_settings)

    def check_params(self):
        if not os.path.exists(self.root_dir):
            raise RootDirNotExist
        if not os.path.exists(self.local_key_folder):
            # logging.getLogger().error("key dir not exist: "+self.key_dir)
            print "key dir not exist: " + self.local_key_folder
            raise LocalKeyFolderNotExist

    def get_local_key_folder(self):
        if self.local_key_folder is None:
            return os.path.join(self.key_dir, "local_keys")
        return self.local_key_folder

    def add_secret_key(self):
        secret_key = self.get_or_create_secret_key(self.get_local_key_folder())
        setattr(base_settings, "SECRET_KEY", secret_key)

    def get_project_path(self):
        if self.project_path is None:
            raise "Root path is not set"
        return self.project_path

    # noinspection PyMethodMayBeStatic
    def is_valid_app_module(self, app_module_folder_full_path):
        signature_filename_list = ["default_settings.py", "default_urls.py"]
        return is_at_least_one_sub_filesystem_item_exists(app_module_folder_full_path, signature_filename_list)
    
    def get_external_apps_folder(self):
        if self.external_apps_folder is None:
            self.external_apps_folder = os.path.join(self.get_project_path(), self.external_app_folder_name)
        return self.external_apps_folder

    def install_auto_detected_apps(self):
        installed_apps = list(getattr(base_settings, "INSTALLED_APPS"))
        
        for folder in os.listdir(self.get_external_apps_folder()):
            app_folder = os.path.join(self.get_external_apps_folder(), folder)
            if os.path.isdir(app_folder):
                for app_module_folder_name in os.listdir(app_folder):
                    app_module_folder_full_path = os.path.join(app_folder, app_module_folder_name)
                    if os.path.isdir(app_module_folder_full_path) and self.is_valid_app_module(app_module_folder_full_path):
                        installed_apps.append(app_module_folder_name)
        setattr(base_settings, "INSTALLED_APPS", tuple(installed_apps))

    def update_installed_apps_etc(self):
        setattr(base_settings, "PROJECT_PATH", self.get_project_path())
        # setattr(base_settings, "TEMPLATE_CONTEXT_PROCESSORS", tuple())
        setattr(base_settings, "DJANGO_AUTO_CONF_LOCAL_DIR", os.path.join(
            self.get_project_path(), self.local_folder_name))
        setattr(base_settings, "STATIC_ROOT", os.path.abspath(os.path.join(self.get_project_path(), 'static')))
        self.install_auto_detected_apps()

    # noinspection PyMethodMayBeStatic
    def get_settings(self):
        return base_settings

    def import_based_on_base_settings(self, module_import_path):
        # ######
        # Inject attributes to builtin and import all other modules
        # Ref: http://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function
        self.init_builtin()
        self.inject_attr()
        try:
            new_base_settings = importlib.import_module(module_import_path)
        except:
            print "Import module error:", module_import_path
            raise
        self.remove_attr()
        update_base_settings(new_base_settings)

    def inject_attr(self):
        self.builtin["PROJECT_ROOT"] = self.root_dir
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            if hasattr(self.builtin, attr):
                raise "Attribute already exists"
            self.builtin[attr] = value

    def remove_attr(self):
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            del self.builtin[attr]

    def init_builtin(self):
        try:
            self.__dict__['builtin'] = sys.modules['__builtin__'].__dict__
        except KeyError:
            self.__dict__['builtin'] = sys.modules['builtins'].__dict__

    def get_existing_secret_key(self, secret_key_folder):
        # from local_keys.secret_key import SECRET_KEY
        m = importlib.import_module("%s.%s.secret_key" % (self.local_folder_name, self.local_key_folder_name))
        logging.info("load existing secret key OK")
        return m.SECRET_KEY


    def create_secret_file_and_get_it(self, local_key_folder):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        ensure_dir(local_key_folder)
        secret_key = get_random_string(50, chars)
        secret_file = open(os.path.join(local_key_folder, 'secret_key.py'), 'w')
        secret_file.write("SECRET_KEY='%s'" % secret_key)
        secret_file.close()
        return self.get_existing_secret_key(local_key_folder)

    def get_or_create_secret_key(self, local_key_folder):
        try:
            return self.get_existing_secret_key(local_key_folder)
        except ImportError:
            print "No existing secret key"
            pass

        try:
            return self.create_secret_file_and_get_it(local_key_folder)
        except Exception:
            print "Try to create secret key failed"
            import traceback

            traceback.print_exc()
            # In case the above not work, use the following.
            # Make this unique, and don't share it with anybody.
            return 'd&amp;x%x+^l@qfxm^2o9x)6ct5*cftlcu8xps9b7l3c$ul*n&amp;%p-k'


def update_base_settings(new_base_settings):
    for attr in dir(new_base_settings):
        if attr != attr.upper():
            continue
        value = getattr(new_base_settings, attr)
        setattr(base_settings, attr, value)
