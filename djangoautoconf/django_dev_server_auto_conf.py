from ufs_tools.app_tools import get_executable_folder
import os
# from ufs_tools import get_folder
# from ufs_tools.inspect_utils import get_parent_frame_file, get_inspection_frame
# from ufs_tools.libtool import include_all_direct_subfolders

from djangoautoconf.django_autoconf import DjangoAutoConf


class DjangoDevServerAutoConf(object):
    def __init__(self):
        self.external_app_repositories = "external_app_repos"
        if "ROOT_DIR" in os.environ:
            self.root_dir = os.environ["ROOT_DIR"]
        else:
            self.root_dir = get_executable_folder()
        self.server_base_package_folder_name = "server_base_packages"
        self.django_auto_conf = DjangoAutoConf()

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir

    def set_external_app_repositories(self, external_app_repositories):
        self.external_app_repositories = external_app_repositories

    def configure(self, extra_settings_folder=None):
        self.django_auto_conf.set_root_dir(self.root_dir)
        self.django_auto_conf.set_external_app_repositories(self.external_app_repositories)
        if not (extra_settings_folder is None):
            self.django_auto_conf.local_app_setting_folders.append(extra_settings_folder)
        self.django_auto_conf.configure()


if __name__ == "__main__":
    d = DjangoDevServerAutoConf()
    print(d)
