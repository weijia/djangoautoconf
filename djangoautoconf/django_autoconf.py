#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import logging
import os
import sys
from django.utils.crypto import get_random_string
import base_settings
from auto_conf_utils import dump_attrs, path_exists, is_at_least_one_sub_filesystem_item_exists
from libtool.basic_lib_tool import is_folder_in_sys_path, include, remove_folder_in_sys_path
from libtool.folder_tool import ensure_dir


log = logging.getLogger(__name__)


class RootDirNotExist(Exception):
    pass


class KeyDirNotExist(Exception):
    pass


class DjangoAutoConf(object):
    def __init__(self, default_settings_import_str=None):
        self.default_settings_import_str = default_settings_import_str
        self.root_dir = None
        # Default keys is located at ../keys relative to universal_settings module?
        self.key_dir = None
        self.extra_settings = []
        self.project_path = None

    def set_default_settings(self, default_settings_import_str):
        self.default_settings_import_str = default_settings_import_str

    def set_root_dir(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        if self.key_dir is None:
            # Default key dir is located in root dir key folder
            self.key_dir = os.path.abspath(os.path.join(root_dir, "keys"))
        self.project_path = os.path.abspath(os.path.abspath(self.root_dir))

    def set_key_dir(self, key_dir):
        self.key_dir = key_dir

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
        if not os.path.exists(self.key_dir):
            # logging.getLogger().error("key dir not exist: "+self.key_dir)
            print "key dir not exist: " + self.key_dir
            raise KeyDirNotExist

    def add_secret_key(self):
        secret_key = get_or_create_secret_key(self.key_dir)
        setattr(base_settings, "SECRET_KEY", secret_key)

    def get_project_path(self):
        return self.project_path

    def is_valid_app_module(self, app_module_folder_full_path):
        signature_filename_list = ["default_settings.py", "default_urls.py"]
        return is_at_least_one_sub_filesystem_item_exists(app_module_folder_full_path, signature_filename_list)

    def install_auto_detected_apps(self):
        installed_apps = list(getattr(base_settings, "INSTALLED_APPS"))
        external_git_folder = os.path.join(self.get_project_path(), "external_git")
        for folder in os.listdir(external_git_folder):
            app_folder = os.path.join(external_git_folder, folder)
            if os.path.isdir(app_folder):
                for app_module_folder_name in os.listdir(app_folder):
                    app_module_folder_full_path = os.path.join(app_folder, app_module_folder_name)
                    if os.path.isdir(app_module_folder_full_path) and self.is_valid_app_module(app_module_folder_full_path):
                        installed_apps.append(app_module_folder_name)
        setattr(base_settings, "INSTALLED_APPS", tuple(installed_apps))

    def update_installed_apps_etc(self):
        setattr(base_settings, "PROJECT_PATH", self.get_project_path())
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


def update_base_settings(new_base_settings):
    for attr in dir(new_base_settings):
        if attr != attr.upper():
            continue
        value = getattr(new_base_settings, attr)
        setattr(base_settings, attr, value)


def get_existing_secret_key(secret_key_folder):
    from keys.local_keys.secret_key import SECRET_KEY

    logging.info("load existing secret key OK")
    return SECRET_KEY


def create_secret_file_and_get_it(local_key_folder):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    ensure_dir(local_key_folder)
    secret_key = get_random_string(50, chars)
    secret_file = open(os.path.join(local_key_folder, 'secret_key.py'), 'w')
    secret_file.write("SECRET_KEY='%s'" % secret_key)
    secret_file.close()
    return get_existing_secret_key(local_key_folder)


def get_or_create_secret_key(key_folder_path):
    local_key_folder = os.path.join(key_folder_path, "local_keys")
    try:
        return get_existing_secret_key(local_key_folder)
    except ImportError:
        print "No existing secret key"
        pass

    try:
        return create_secret_file_and_get_it(local_key_folder)
    except Exception:
        print "Try to create secret key failed"
        import traceback

        traceback.print_exc()
        # In case the above not work, use the following.
        # Make this unique, and don't share it with anybody.
        return 'd&amp;x%x+^l@qfxm^2o9x)6ct5*cftlcu8xps9b7l3c$ul*n&amp;%p-k'