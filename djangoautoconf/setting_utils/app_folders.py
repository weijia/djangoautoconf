import os

from djangoautoconf.auto_conf_utils import enum_folders
from djangoautoconf.setting_utils.app_module_utils import is_valid_app_module


class AppFolderUtil(object):
    EXTERNAL_APP_REPO_ROOT_RELATIVE_PATH = "external_app_repos"

    def __init__(self, root_full_path):
        super(AppFolderUtil, self).__init__()
        self.root_full_path = root_full_path

    def enum_app_folders(self):
        for app_module_folder in self._enum_app_module_folders():
            if is_valid_app_module(app_module_folder):
                # app_module_folder_name = os.path.basename(app_module_folder)
                app_root_folder = os.path.dirname(app_module_folder)
                yield app_root_folder

    def _enum_app_module_folders(self):
        for app_root_folder in self._enum_app_root_folders_in_repo():
            for app_module_folder in enum_folders(app_root_folder):
                yield app_module_folder

    def _enum_app_root_folders_in_repo(self):
        for repo in self._get_external_apps_repositories():
            for apps_root_folder in enum_folders(repo):
                yield apps_root_folder

    def _get_external_apps_repositories(self):
        return [os.path.join(self.root_full_path, self.EXTERNAL_APP_REPO_ROOT_RELATIVE_PATH)]

