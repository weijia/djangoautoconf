import sys
from django.utils import importlib


class ConfigurableAttributeGetter(object):
    def __init__(self, module_of_attribute, default_module=None):
        super(ConfigurableAttributeGetter, self).__init__()
        self.module_of_attribute = module_of_attribute
        self.default_module = default_module

    def get_module_of_local_keys(self):
        exception = None
        for module_path in ["local.local_keys", "keys.local_keys"]:
            try:
                m = importlib.import_module("%s.%s" % (module_path, self.module_of_attribute))
                return m
            except ImportError, e:
                exception = e
        raise exception

    def get_attr(self, attr_name):
        try:
            m = self.get_module_of_local_keys()
            # return getattr(m, attr_name)
        except ImportError:
            # from management.commands.keys_default.admin_pass import default_admin_password, default_admin_user
            if self.default_module is None:
                m = importlib.import_module("%s_template" % self.module_of_attribute)
            else:
                m = importlib.import_module("%s.%s_template" % (self.default_module, self.module_of_attribute))
        return getattr(m, attr_name)


def get_local_key(key_name, default_module=None):
    """
    Get local setting for the keys.
    :param key_name: module path: admin_account.admin_user
    :param default_module: If the template can not be directly imported, use this to specify the parent module.
    :return: value for the key
    """
    key_name_module_path = key_name.split(".")
    module_name = ".".join(key_name_module_path[0:-1])
    attr_name = key_name_module_path[-1]
    c = ConfigurableAttributeGetter(module_name, default_module)
    return c.get_attr(attr_name)
