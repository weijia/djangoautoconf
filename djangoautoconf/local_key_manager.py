import importlib


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
            except ImportError as e:
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


class ModuleAndVarNameShouldNotHaveDashCharacter(Exception):
    pass


def get_local_key(module_and_var_name, default_module=None):
    """
    Get local setting for the keys.
    :param module_and_var_name: for example: admin_account.admin_user, then you need to put admin_account.py in
        local/local_keys/ and add variable admin_user="real admin username", module_name_and_var_name should not
        contain "-" because
    :param default_module: If the template can not be directly imported, use this to specify the parent module.
    :return: value for the key
    """
    if "-" in module_and_var_name:
        raise ModuleAndVarNameShouldNotHaveDashCharacter
    key_name_module_path = module_and_var_name.split(".")
    module_name = ".".join(key_name_module_path[0:-1])
    attr_name = key_name_module_path[-1]
    c = ConfigurableAttributeGetter(module_name, default_module)
    return c.get_attr(attr_name)


def get_default_admin_password():
    return get_local_key("admin_account.admin_password", "djangoautoconf.keys_default")


def get_default_admin_username():
    return get_local_key("admin_account.admin_username", "djangoautoconf.keys_default")

