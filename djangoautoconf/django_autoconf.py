#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import logging
import os

import django
from ufs_tools import get_folder, sys
from ufs_tools.app_tools import get_executable_folder
from ufs_tools.inspect_utils import get_inspection_frame
from ufs_tools.libtool import include_all_direct_subfolders, exclude

from .auto_conf_utils import dump_attrs, is_at_least_one_sub_filesystem_item_exists, enum_folders
from .django_setting_manager import DjangoSettingManager
from ufs_tools.basic_lib_tool import remove_folder_in_sys_path, include

from djangoautoconf.base_setting_storage import ObjectSettingStorage

log = logging.getLogger(__name__)


class RootDirNotExist(Exception):
    pass


class LocalKeyFolderNotExist(Exception):
    pass


class DjangoAutoConf(DjangoSettingManager):
    """
    external_app_repos
        repo folder
            server app folders/modules may be imported
    """
    AUTO_DETECT_CONFIG_FILENAME = "default_settings.py"

    def __init__(self, default_settings_import_str=None):
        super(DjangoAutoConf, self).__init__(default_settings_import_str)
        # Default keys is located at ../keys relative to universal_settings module?
        # self.extra_settings_in_base_package_folder = "others/extra_settings"  # base extra setting
        self.key_dir = None
        self.local_key_folder = None
        self.extra_setting_module_full_names = []
        self.project_path = None
        self.server_base_package_folder = "server_base_packages"
        self.local_key_folder_relative_to_root = os.path.join(self.local_folder_name, self.local_key_folder_name)
        self.external_apps_folder = None
        self.installed_app_list = None
        self.external_app_repositories = None
        self.external_app_repositories_full_path = None
        self.external_app_folder_name = None

    def get_full_path(self, relative_path):
        return os.path.join(self.root_dir, relative_path)

    def set_external_app_repositories(self, external_app_repositories):
        if os.path.isabs(external_app_repositories):
            # print external_app_repositories
            self.external_app_repositories_full_path = external_app_repositories
        else:
            # print self.root_dir, external_app_repositories, "not abs"
            self.external_app_repositories_full_path = os.path.join(self.root_dir, external_app_repositories)
        self.external_app_repositories = external_app_repositories
        # self.add_extra_setting_relative_folder_for_repo(external_app_repositories)
        logging.debug("Added: " + external_app_repositories)
        full_path_of_repo_root = self.get_full_path(external_app_repositories)
        for folder_full_path in enum_folders(full_path_of_repo_root):
            if os.path.isdir(folder_full_path):
                logging.debug("Scanning: " + folder_full_path)
                include_all_direct_subfolders(folder_full_path)

    def set_external_app_folder_name(self, external_app_folder_name):
        self.external_app_folder_name = external_app_folder_name

    def set_root_dir(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.project_path = os.path.abspath(os.path.abspath(self.root_dir))
        self.local_key_folder = os.path.join(self.root_dir, self.local_key_folder_relative_to_root)
        self.local_app_setting_folders.append(os.path.join(self.root_dir, self.local_settings_relative_folder))
        self.setting_storage = ObjectSettingStorage(self.root_dir)

    def set_key_dir(self, key_dir):
        self.key_dir = key_dir
        self.local_key_folder = os.path.join(self.key_dir, self.local_key_folder_name)

    def set_local_key_folder(self, local_key_folder):
        self.local_key_folder = local_key_folder

    def configure(self, features=[]):
        self.__check_params()
        self.set_settings_env()
        self.load_settings_in_project_template()
        self.set_project_folders_in_settings()
        self.load_all_extra_settings(features)
        self.setting_storage.add_secret_key(self.get_or_create_secret_key(self.get_local_key_folder()))
        self.update_installed_apps_etc()
        # self.setting_storage.remove_empty_list()
        self.setting_storage.refine_attributes()
        dump_attrs(self.setting_storage.get_settings())

    @staticmethod
    def exe():
        from django.core.management import execute_from_command_line
        argv = sys.argv
        if argv[0] == "manage.exe":
            argv = [""].extend(argv)
        execute_from_command_line(argv)

    @staticmethod
    def set_settings_env(executable_folder=None):
        """
        Add all application folders
        :param executable_folder: the folder that contains local and external_app_repos
        :return:
        """
        executable_folder = executable_folder or get_executable_folder()
        # print "!!!!!!!!!!!!!! executable:", executable_folder
        if os.path.exists(os.path.join(executable_folder, "local/total_settings.py")):
            print("Using total settings")
            os.chdir(executable_folder)
            os.environ["DJANGO_SETTINGS_MODULE"] = "local.total_settings"
            os.environ["STATIC_ROOT"] = os.path.join(executable_folder, "static")
            os.environ["MEDIA_ROOT"] = os.path.join(executable_folder, "media")
        else:
            os.environ.setdefault('ROOT_DIR', get_folder(get_inspection_frame(2)))
            os.environ["DJANGO_SETTINGS_MODULE"] = "djangoautoconf.base_settings"

    def __check_params(self):
        if not os.path.exists(self.root_dir):
            raise RootDirNotExist
        if not os.path.exists(self.local_key_folder):
            # logging.getLogger().error("key dir not exist: "+self.key_dir)
            print("key dir not exist: " + self.local_key_folder)
            raise LocalKeyFolderNotExist

    def get_local_key_folder(self):
        if self.local_key_folder is None:
            return os.path.join(self.key_dir, "local_keys")
        return self.local_key_folder

    def get_project_path(self):
        if self.project_path is None:
            raise "Root path is not set"
        return self.project_path

    # noinspection PyMethodMayBeStatic
    def is_valid_app_module(self, app_module_folder_full_path):
        signature_filename_list = [self.AUTO_DETECT_CONFIG_FILENAME, "default_urls.py", "urls.py"]
        return os.path.isdir(app_module_folder_full_path) and is_at_least_one_sub_filesystem_item_exists(
            app_module_folder_full_path, signature_filename_list)

    def get_external_apps_folder(self):
        if self.external_apps_folder is None:
            self.external_apps_folder = os.path.join(self.get_project_path(), self.external_app_folder_name)
        return self.external_apps_folder

    def get_external_apps_repositories(self):
        if self.external_app_repositories_full_path is None:
            return [self.get_external_apps_folder(), ]
        else:
            return enum_folders(self.external_app_repositories_full_path)

    def enum_app_root_folders_in_repo(self):
        for repo in self.get_external_apps_repositories():
            for apps_root_folder in enum_folders(repo):
                yield apps_root_folder

    def enum_app_module_folders(self):
        for app_root_folder in self.enum_app_root_folders_in_repo():
            for app_module_folder in enum_folders(app_root_folder):
                yield app_module_folder

    def install_auto_detected_apps(self):
        self.installed_app_list = self.setting_storage.get_installed_apps()
        for app_module_folder in self.enum_app_module_folders():
            if self.is_valid_app_module(app_module_folder):
                app_module_folder_name = os.path.basename(app_module_folder)
                app_root_folder = os.path.dirname(app_module_folder)
                include(app_root_folder)
                self.installed_app_list.append(app_module_folder_name)
        self.setting_storage.set_attr("INSTALLED_APPS", tuple(self.installed_app_list))

    def update_installed_apps_etc(self):
        self.install_auto_detected_apps()

    def set_project_folders_in_settings(self):
        self.setting_storage.set_attr("PROJECT_PATH", self.get_project_path())
        # setattr(base_settings, "TEMPLATE_CONTEXT_PROCESSORS", tuple())
        self.setting_storage.set_attr("DJANGO_AUTO_CONF_LOCAL_DIR", os.path.join(
            self.get_project_path(), self.local_folder_name))
        self.setting_storage.set_attr("STATIC_ROOT", os.path.abspath(os.path.join(self.get_project_path(), 'static')))

    def load_all_extra_settings(self, features):
        self.update_base_settings_with_features(features)
        self.load_extra_settings_in_folders()
        self.__load_default_setting_from_apps()

    def __load_default_setting_from_apps(self):
        for app_module_folder in self.enum_app_module_folders():
            default_settings_full_path = os.path.join(app_module_folder, self.AUTO_DETECT_CONFIG_FILENAME)
            if os.path.exists(default_settings_full_path) and not os.path.isdir(default_settings_full_path):
                app_module_folder_name = os.path.basename(app_module_folder)
                app_root_folder = os.path.dirname(app_module_folder)
                include(app_root_folder)
                self.setting_storage.import_based_on_base_settings(
                    "%s.%s" % (app_module_folder_name,
                               self.AUTO_DETECT_CONFIG_FILENAME.split(
                                   ".")[0]))
                remove_folder_in_sys_path(app_root_folder)

    def load_settings_in_project_template(self):
        if self.setting_storage.is_above_or_equal_to_django1_11():
            full_path = os.path.join(get_folder(django.__file__), "conf/project_template/project_name/settings.py-tpl")
            f = open(full_path)
            module_content = f.read()
            self.setting_storage.eval_content(module_content)
        else:
            template_root = os.path.join(get_folder(django.__file__), "conf/project_template/")
            include(template_root)
            self.setting_storage.import_based_on_base_settings("project_name.settings")
            exclude(template_root)
