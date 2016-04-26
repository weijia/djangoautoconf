import importlib
import logging
import os
import sys
from sys import modules as sys_modules
from django.utils.crypto import get_random_string
import base_settings
from djangoautoconf.auto_conf_utils import enum_modules, enum_folders
from libtool import include
from libtool.basic_lib_tool import remove_folder_in_sys_path
from libtool.folder_tool import ensure_dir

__author__ = 'weijia'

log = logging.getLogger(__name__)


def update_base_settings(new_base_settings):
    for attr in dir(new_base_settings):
        if attr != attr.upper():
            continue
        value = getattr(new_base_settings, attr)
        setattr(base_settings, attr, value)
    logging.debug(base_settings.INSTALLED_APPS)


class DjangoSettingManager(object):
    def __init__(self, default_settings_import_str=None):
        super(DjangoSettingManager, self).__init__()
        self.local_folder_name = "local"
        self.local_key_folder_name = "local_keys"
        self.root_dir = None
        self.other_external_setting_folder = "others/external_settings"
        self.base_extra_setting_list = ["extra_settings.settings"]
        self.default_settings_import_str = default_settings_import_str
        self.extra_setting_folders = []
        self.external_settings_root_folder_name = "others"
        self.external_settings_folder_name = "external_settings"
        self.local_settings_relative_folder = "local/local_settings"
        self.external_app_folder_name = "external_apps"
        self.local_app_setting_folders = []

    def add_extra_setting_full_path_folder(self, extra_setting_folder):
        self.extra_setting_folders.append(extra_setting_folder)

    # noinspection PyMethodMayBeStatic
    def get_settings(self):
        return base_settings

    def add_extra_setting_relative_folder_for_repo(self, repo_folder):
        if self.root_dir is None:
            raise "Please set root first"

        repo_root = os.path.join(self.root_dir, repo_folder)
        for app_folder in enum_folders(repo_root):
            logging.debug("Processing: " + app_folder)
            app_full_path = app_folder  # os.path.join(repo_root, app_folder)
            repo_extra_setting_folder = os.path.join(app_full_path, self.other_external_setting_folder)
            if os.path.exists(repo_extra_setting_folder):
                logging.debug("Added: " + repo_extra_setting_folder)
                self.add_extra_setting_full_path_folder(repo_extra_setting_folder)

    def load_extra_settings_in_folders(self):
        # Add local/local_settings/ folder
        self.extra_setting_folders.extend(self.local_app_setting_folders)
        for folder in self.extra_setting_folders:
            include(folder)
            for module_name in enum_modules(folder):
                logging.debug("---------------------------------------Processing: " + module_name)
                self.import_based_on_base_settings(module_name)
            remove_folder_in_sys_path(folder)

    def update_base_settings_with_features(self, features):
        ordered_import_list = self.get_feature_setting_module_list(features)
        for one_setting in ordered_import_list:
            self.import_based_on_base_settings(one_setting)

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
        self.__remove_attr()
        update_base_settings(new_base_settings)
        del sys_modules[module_import_path]

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

    def get_feature_setting_module_list(self, features):
        ordered_import_list = [self.default_settings_import_str,
                               "djangoautoconf.sqlite_database"
                               # "djangoautoconf.mysql_database"
                               ]
        for feature in features:
            ordered_import_list.append("djangoautoconf.features." + feature)

        ordered_import_list.append("server_base_packages.others.extra_settings.settings")

        return ordered_import_list

    @staticmethod
    def remove_empty_list():
        for attr in dir(base_settings):
            value = getattr(base_settings, attr)
            if (type(value) is list) and len(value) == 0:
                delattr(base_settings, attr)

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

    @staticmethod
    def remove_duplicated(value_in_tuple):
        new_tuple = []
        for i in value_in_tuple:
            if not (i in new_tuple):
                new_tuple.append(i)
        return new_tuple

    def refine_attributes(self, s):
        for attr in dir(s):
            if attr != attr.upper():
                continue
            value = getattr(s, attr)
            if type(value) is tuple:
                setattr(s, attr, self.remove_duplicated(value))


# Ref: http://stackoverflow.com/questions/1668223/how-to-de-import-a-python-module
def delete_module(modname, paranoid=None):
    from sys import modules
    try:
        this_module = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(this_module)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass
