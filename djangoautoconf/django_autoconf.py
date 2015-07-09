#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import logging
import os
import sys

from django.utils.crypto import get_random_string
import re

import base_settings
from auto_conf_utils import dump_attrs, is_at_least_one_sub_filesystem_item_exists, enum_folders
from libtool import include, include_all_direct_subfolders
from libtool.folder_tool import ensure_dir
from django_setting_manager import DjangoSettingManager

log = logging.getLogger(__name__)


class RootDirNotExist(Exception):
    pass


class LocalKeyFolderNotExist(Exception):
    pass


class DjangoAutoConf(DjangoSettingManager):
    def __init__(self, default_settings_import_str=None):
        super(DjangoAutoConf, self).__init__(default_settings_import_str)
        # Default keys is located at ../keys relative to universal_settings module?
        self.extra_settings_in_base_package_folder = "others/extra_settings"
        self.key_dir = None
        self.local_key_folder = None
        self.extra_setting_module_full_names = []
        self.project_path = None
        self.local_key_folder_name = "local_keys"
        self.server_base_package_folder = "server_base_packages"
        self.local_folder_name = "local"
        self.local_key_folder_relative_to_root = os.path.join(self.local_folder_name, self.local_key_folder_name)
        self.external_apps_folder = None
        self.installed_app_list = None
        self.external_app_repositories = None

    def get_full_path(self, relative_path):
        return os.path.join(self.root_dir, relative_path)

    def set_external_app_repositories(self, external_app_repositories):
        self.external_app_repositories = external_app_repositories
        self.add_extra_setting_relative_folder_for_repo(external_app_repositories)
        logging.debug("Added: "+external_app_repositories)
        full_path_of_repo_root = self.get_full_path(external_app_repositories)
        for folder in enum_folders(full_path_of_repo_root):
            logging.debug("Scanning: "+folder)
            scanning_folder_full_path = os.path.join(full_path_of_repo_root, folder)
            if os.path.isdir(scanning_folder_full_path):
                include_all_direct_subfolders(scanning_folder_full_path)

    def set_external_app_folder_name(self, external_app_folder_name):
        self.external_app_folder_name = external_app_folder_name

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

    def configure(self, features=[]):
        self.check_params()
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoautoconf.base_settings")
        os.environ["DJANGO_SETTINGS_MODULE"] = "djangoautoconf.base_settings"

        self.load_all_extra_settings(features)
        self.add_secret_key()
        self.update_installed_apps_etc()
        self.remove_empty_list()
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
        signature_filename_list = ["default_settings.py", "default_urls.py", "urls.py"]
        return is_at_least_one_sub_filesystem_item_exists(app_module_folder_full_path, signature_filename_list)
    
    def get_external_apps_folder(self):
        if self.external_apps_folder is None:
            self.external_apps_folder = os.path.join(self.get_project_path(), self.external_app_folder_name)
        return self.external_apps_folder

    def get_external_apps_repositories(self):
        if self.external_app_repositories is None:
            return [self.get_external_apps_folder(),]
        else:
            return enum_folders(self.external_app_repositories)

    def install_auto_detected_apps(self):
        self.installed_app_list = list(getattr(base_settings, "INSTALLED_APPS"))

        for repo in self.get_external_apps_repositories():
            for apps_root_folder in enum_folders(repo):
                self.scan_apps_in_sub_folders(apps_root_folder)

        setattr(base_settings, "INSTALLED_APPS", tuple(self.installed_app_list))

    def scan_apps_in_sub_folders(self, apps_root_folder):
        add_apps_root_folder_to_sys_path = False
        if os.path.isdir(apps_root_folder):
            for app_module_folder_name in os.listdir(apps_root_folder):
                app_module_folder_full_path = os.path.join(apps_root_folder, app_module_folder_name)
                if os.path.isdir(app_module_folder_full_path) and \
                        self.is_valid_app_module(app_module_folder_full_path):
                    add_apps_root_folder_to_sys_path = True
                    self.installed_app_list.append(app_module_folder_name)
        if add_apps_root_folder_to_sys_path:
            include(apps_root_folder)

    def update_installed_apps_etc(self):
        setattr(base_settings, "PROJECT_PATH", self.get_project_path())
        # setattr(base_settings, "TEMPLATE_CONTEXT_PROCESSORS", tuple())
        setattr(base_settings, "DJANGO_AUTO_CONF_LOCAL_DIR", os.path.join(
            self.get_project_path(), self.local_folder_name))
        setattr(base_settings, "STATIC_ROOT", os.path.abspath(os.path.join(self.get_project_path(), 'static')))
        self.install_auto_detected_apps()

    def get_existing_secret_key(self, secret_key_folder):
        # from local_keys.secret_key import SECRET_KEY
        log.debug("importing key from %s.%s.secret_key" % (self.local_folder_name, self.local_key_folder_name))
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


