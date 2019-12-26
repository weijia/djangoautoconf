import importlib
import logging
import os

from django.utils.crypto import get_random_string
from .auto_conf_utils import enum_modules, enum_folders
from ufs_tools.basic_lib_tool import remove_folder_in_sys_path, include
from ufs_tools.folder_tool import ensure_dir

__author__ = 'weijia'

log = logging.getLogger(__name__)


def get_feature_setting_module_list(features):
    # TODO: combine default settings in 3 places, djangoautoconf.features.djangoautoconf_settings, base_settings,
    # TODO: and base_settings_storage
    ordered_import_list = [
        # self.default_settings_import_str,
        "djangoautoconf.djangoautoconf_settings",
        # "djangoautoconf.mysql_database"
    ]
    for feature in features:
        ordered_import_list.append("djangoautoconf.features." + feature)

    # ordered_import_list.append("server_base_packages.others.extra_settings.settings")

    return ordered_import_list


class DjangoSettingManager(object):
    local_settings_relative_folder = "local/local_settings"
    local_folder_name = "local"
    local_key_folder_name = "local_keys"

    def __init__(self, default_settings_import_str=None):
        super(DjangoSettingManager, self).__init__()
        self.root_dir = None
        self.default_settings_import_str = default_settings_import_str
        self.extra_setting_folders = []
        self.local_app_setting_folders = []
        if "EXTRA_SETTING_FOLDER" in os.environ and os.environ["EXTRA_SETTING_FOLDER"]:
            self.local_app_setting_folders.append(os.environ["EXTRA_SETTING_FOLDER"])
        self.setting_storage = None

    def add_extra_setting_full_path_folder(self, extra_setting_folder):
        self.extra_setting_folders.append(extra_setting_folder)

    def load_extra_settings_in_folders(self):
        # Add local/local_settings/ folder
        self.extra_setting_folders.extend(self.local_app_setting_folders)
        for folder in self.extra_setting_folders:
            include(folder)
            for module_name in enum_modules(folder):
                logging.debug("---------------------------------------Processing: " + module_name)
                self.setting_storage.import_based_on_base_settings(module_name)
            remove_folder_in_sys_path(folder)

    def update_base_settings_with_features(self, features):
        ordered_import_list = get_feature_setting_module_list(features)
        for one_setting in ordered_import_list:
            self.setting_storage.import_based_on_base_settings(one_setting)

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
            print("No existing secret key")
            pass
        except ModuleNotFoundError:
            print("No existing secret key")
            pass

        try:
            return self.create_secret_file_and_get_it(local_key_folder)
        except Exception:
            print("Try to create secret key failed")
            import traceback

            traceback.print_exc()
            # In case the above not work, use the following.
            # Make this unique, and don't share it with anybody.
            return 'd&amp;x%x+^l@qfxm^2o9x)6ct5*cftlcu8xps9b7l3c$ul*n&amp;%p-k'
