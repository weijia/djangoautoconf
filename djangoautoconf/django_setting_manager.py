import importlib
import sys
from djangoautoconf.auto_conf_utils import enum_modules, enum_folders
from libtool import include
from libtool.basic_lib_tool import remove_folder_in_sys_path

__author__ = 'weijia'
import os
import base_settings


def update_base_settings(new_base_settings):
    for attr in dir(new_base_settings):
        if attr != attr.upper():
            continue
        value = getattr(new_base_settings, attr)
        setattr(base_settings, attr, value)


class DjangoSettingManager(object):
    def __init__(self, default_settings_import_str=None):
        super(DjangoSettingManager, self).__init__()
        self.root_dir = None
        self.other_external_setting_folder = "others/external_settings"
        self.base_extra_setting_list = ["extra_settings.settings"]
        self.default_settings_import_str = default_settings_import_str
        self.extra_setting_folders = []
        self.external_settings_root_folder_name = "others"
        self.external_settings_folder_name = "external_settings"
        self.local_settings_relative_folder = "local/local_settings"
        self.external_app_folder_name = "external_apps"
        self.local_app_setting_folder = None

    # def set_base_extra_settings_list(self, base_extra_settings):
    #     self.base_extra_setting_list = base_extra_settings

    def add_extra_setting_full_path_folder(self, extra_setting_folder):
        self.extra_setting_folders.append(extra_setting_folder)

    # def get_extra_settings(self):
    #     pass

    # noinspection PyMethodMayBeStatic
    def get_settings(self):
        return base_settings

    def load_all_extra_settings(self, features):
        self.__update_base_settings_with_features(features)
        self.__load_extra_settings_in_folders()

    def add_extra_setting_relative_folder_for_repo(self, repo_folder):
        if self.root_dir is None:
            raise "Please set root first"

        repo_root = os.path.join(self.root_dir, repo_folder)
        for app_folder in enum_folders(repo_root):
            app_full_path = os.path.join(repo_root, app_folder)
            repo_extra_setting_folder = os.path.join(app_full_path, self.other_external_setting_folder)
            if os.path.exists(repo_extra_setting_folder):
                self.add_extra_setting_full_path_folder(repo_extra_setting_folder)

    def __load_extra_settings_in_folders(self):
        # Add local/local_settings/ folder
        self.extra_setting_folders.insert(0, self.local_app_setting_folder)
        for folder in self.extra_setting_folders:
            include(folder)
            for module_name in enum_modules(folder):
                self.__import_based_on_base_settings(module_name)
            remove_folder_in_sys_path(folder)

    def __update_base_settings_with_features(self, features):
        ordered_import_list = self.get_feature_setting_module_list(features)
        for one_setting in ordered_import_list:
            self.__import_based_on_base_settings(one_setting)

    def __import_based_on_base_settings(self, module_import_path):
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
        self.__remove_attr()
        update_base_settings(new_base_settings)

    def __inject_attr(self):
        self.builtin["PROJECT_ROOT"] = self.root_dir
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            if hasattr(self.builtin, attr):
                raise "Attribute already exists"
            self.builtin[attr] = value

    def __remove_attr(self):
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            del self.builtin[attr]

    def __init_builtin(self):
        try:
            self.__dict__['builtin'] = sys.modules['__builtin__'].__dict__
        except KeyError:
            self.__dict__['builtin'] = sys.modules['builtins'].__dict__

    # def get_folder_for_settings_in_external_apps_folder(self):
    #     external_settings_root_folder = os.path.join(self.get_external_apps_folder(),
    #         self.external_settings_root_folder_name)
    #     folder_for_external_apps_settings = os.path.join(external_settings_root_folder,
    #                                                      self.external_settings_folder_name)
    #     return folder_for_external_apps_settings

    # def add_extra_settings_from_folder(self, local_setting_dir=None):
    #     extra_setting_list = self.base_extra_setting_list
    #     if local_setting_dir is None:
    #         local_setting_dir = self.local_app_setting_folder
    #     for module_name in enum_modules(local_setting_dir):
    #         extra_setting_list.append("local.local_settings.%s" % module_name)
    #
    #     # Add external settings in external apps folder
    #     settings_folder_in_external_apps_folder = self.get_folder_for_settings_in_external_apps_folder()
    #     if os.path.exists(settings_folder_in_external_apps_folder):
    #         for module_name in self.enum_modules(settings_folder_in_external_apps_folder):
    #             extra_setting_list.append("%s.%s" % (self.external_settings_folder_name, module_name))
    #     self.__add_extra_settings(extra_setting_list)

    def get_feature_setting_module_list(self, features):
        ordered_import_list = [self.default_settings_import_str,
                               "djangoautoconf.sqlite_database"
                               # "djangoautoconf.mysql_database"
        ]
        for feature in features:
            ordered_import_list.append("djangoautoconf.features." + feature)

        ordered_import_list.append("server_base_packages.others.extra_settings.settings")

        return ordered_import_list
