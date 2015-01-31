from django.utils import importlib

__author__ = 'q19420'


def get_local_key(key_name, default_module=None):
    key_name_module_path = key_name.split(".")
    module_name = key_name_module_path[0]
    attr_name = key_name_module_path[1]
    try:
        m = importlib.import_module("keys.local_keys.%s" % module_name)
        #return getattr(m, attr_name)
    except ImportError:
        #from management.commands.keys_default.admin_pass import default_admin_password, default_admin_user
        if default_module is None:
            m = __import__("%s_template" % module_name)
        else:
            m = __import__("%s.%s_template" % module_name)
    return getattr(m, attr_name)