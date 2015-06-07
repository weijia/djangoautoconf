import importlib
import sys
from djangoautoconf.auto_conf_utils import enum_modules

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
        self.base_extra_setting_list = ["extra_settings.settings"]
        self.default_settings_import_str = default_settings_import_str
        self.extra_setting_folders = []
        self.external_settings_root_folder_name = "others"
        self.external_settings_folder_name = "external_settings"
        self.local_settings_relative_folder = "local/local_settings"
        self.external_app_folder_name = "external_apps"

    def set_base_extra_settings_list(self, base_extra_settings):
        self.base_extra_setting_list = base_extra_settings

    # def get_extra_settings(self):
    #     pass

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

    def get_folder_for_settings_in_external_apps_folder(self):
        external_settings_root_folder = os.path.join(self.get_external_apps_folder(),
            self.external_settings_root_folder_name)
        folder_for_external_apps_settings = os.path.join(external_settings_root_folder,
                                                         self.external_settings_folder_name)
        return folder_for_external_apps_settings

    def add_extra_settings_from_folder(self, local_setting_dir=None):
        extra_setting_list = self.base_extra_setting_list
        if local_setting_dir is None:
            local_setting_dir = self.local_app_setting_folder
        for module_name in enum_modules(local_setting_dir):
            extra_setting_list.append("local.local_settings.%s" % module_name)

        # Add external settings in external apps folder
        settings_folder_in_external_apps_folder = self.get_folder_for_settings_in_external_apps_folder()
        if os.path.exists(settings_folder_in_external_apps_folder):
            for module_name in self.enum_modules(settings_folder_in_external_apps_folder):
                extra_setting_list.append("%s.%s" % (self.external_settings_folder_name, module_name))
        self.add_extra_settings(extra_setting_list)

    def add_extra_settings(self, extra_setting_list):
        self.extra_setting_module_full_names.extend(extra_setting_list)

    def get_setting_module_list(self, features):
        ordered_import_list = [self.default_settings_import_str,
                               "djangoautoconf.sqlite_database"
                               # "djangoautoconf.mysql_database"
        ]
        ordered_import_list.extend(self.extra_setting_module_full_names)
        for feature in features:
            self.ordered_import_list.append("djangoautoconf.features." + feature)
        return ordered_import_list
