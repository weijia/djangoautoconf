from ufs_tools import get_folder, os
from ufs_tools.inspect_utils import get_parent_frame_file, get_inspection_frame
from ufs_tools.libtool import include_all_direct_subfolders

from djangoautoconf import DjangoAutoConf


class DjangoDevServerAutoConf(object):
    def __init__(self):
        self.default_settings = "default_django_15_and_below.settings"
        self.external_app_repositories = "external_app_repos"
        if os.environ["ROOT_DIR"]:
            self.root_dir = os.environ["ROOT_DIR"]
        else:
            self.root_dir = get_folder(get_inspection_frame(2))
        self.server_base_package_folder_name = "server_base_packages"
        self.django_auto_conf = DjangoAutoConf()

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir

    def set_external_app_repositories(self, external_app_repositories):
        self.external_app_repositories = external_app_repositories

    def set_default_settings(self, default_settings):
        self.default_settings = default_settings

    def configure(self, extra_settings_folder=None):
        self.django_auto_conf.set_root_dir(self.root_dir)
        self.django_auto_conf.set_external_app_repositories(self.external_app_repositories)
        self.django_auto_conf.set_default_settings(self.default_settings)
        if not (extra_settings_folder is None):
            self.django_auto_conf.local_app_setting_folders.append(extra_settings_folder)
        self.django_auto_conf.configure()


if __name__ == "__main__":
    d = DjangoDevServerAutoConf()
    print d
