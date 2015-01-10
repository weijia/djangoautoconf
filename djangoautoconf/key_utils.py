__author__ = 'weijia'


def get_local_keys(key_module_name, key_name):
    try:
        module = __import__("keys.%s" % key_module_name)
        return getattr(module, key_name)
    except ImportError:
        module = __import__("keys_template.%s" % key_module_name)
        return getattr(module, key_name)
