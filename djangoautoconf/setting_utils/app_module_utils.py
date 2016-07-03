
import os

from djangoautoconf.auto_conf_utils import is_at_least_one_sub_filesystem_item_exists

AUTO_DETECT_CONFIG_FILENAME = "default_settings.py"


def is_valid_app_module(app_module_folder_full_path):
    signature_filename_list = [AUTO_DETECT_CONFIG_FILENAME, "default_urls.py", "urls.py"]
    return os.path.isdir(app_module_folder_full_path) and is_at_least_one_sub_filesystem_item_exists(
        app_module_folder_full_path, signature_filename_list)
