import importlib
import logging
import os
import re

log = logging.getLogger(__name__)


def inject_attributes(target_class, src_module, exclude=None):
    exclude = exclude or []
    target_instance = target_class()
    for attr in dir(src_module):
        if attr != attr.upper():
            continue
        if attr in exclude:
            continue
        value = getattr(src_module, attr)
        setattr(target_instance.__class__, attr, value)
        # print "setting attr:", attr, value


def dump_attrs(obj_instance):
    for attr in dir(obj_instance):
        if attr != attr.upper():
            continue
        value = getattr(obj_instance, attr)
        log.debug(u"%s: %s" % (attr, value))


def get_class(django_cb_class_full_name):
    settings_module = importlib.import_module(get_module_name_from_str(django_cb_class_full_name))
    # print settings_module
    # print getattr(settings_module, get_class_name_from_str(settings_class_str))
    return getattr(settings_module, get_class_name_from_str(django_cb_class_full_name))().__class__
    # return getattr(settings_module, get_settings_class_name()).__class__


def get_module_name_from_str(importing_class_name):
    # print importing_class_name.rsplit('.', 1)[0]
    return importing_class_name.rsplit('.', 1)[0]


def get_class_name_from_str(importing_class_name):
    # print importing_class_name.rsplit('.', 1)[1]
    return importing_class_name.rsplit('.', 1)[1]


def validate_required_attributes(setting_class_instance):
    if setting_class_instance.DATABASES["default"]["ENGINE"] == 'django.db.backends.dummy':
        raise "Invalid database"


def path_exists(path):
    return os.path.exists(path)


def is_at_least_one_sub_filesystem_item_exists(full_path, filename_list):
    for filename in filename_list:
        target_path = os.path.join(full_path, filename)
        if os.path.isdir(full_path) and path_exists(target_path):
            return True
    return False


def get_module_path(mod):
    if os.path.basename(mod.__file__) != "__init__.pyc" and os.path.basename(mod.__file__) != "__init__.py":
        return get_source_filename(mod.__file__)
    return os.path.dirname(mod.__file__)


def get_source_filename(compiled_name):
    return compiled_name.replace("pyc", "py")


def get_module_file_path(mod):
    return get_source_filename(mod.__file__)


def get_module_filename(mod):
    return get_source_filename(os.path.basename(mod.__file__))


def get_module_include_files_config(mod, prefix=None):
    if prefix is None:
        return get_module_file_path(mod), get_module_filename(mod)
    else:
        return get_module_file_path(mod), os.path.join(prefix, get_module_filename(mod))


def enum_folders(parent_folder):
    logging.debug("Listing folder: "+parent_folder)
    for folder in os.listdir(parent_folder):
        full_path = os.path.join(parent_folder, folder)
        if os.path.isdir(full_path):
            yield full_path


def enum_modules(folder):
    for filename in os.listdir(folder):
        is_py = re.search(r'\.py$', filename)
        if is_py and (filename != "__init__.py"):
            yield filename.replace(".py", "")
