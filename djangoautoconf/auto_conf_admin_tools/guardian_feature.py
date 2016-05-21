from django.contrib.admin import ModelAdmin

from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'
from django.conf import settings


class GuardianFeature(AdminFeatureBase):

    def __init__(self):
        super(GuardianFeature, self).__init__()
        self.is_guardian_supported = False

        if "guardian" in settings.INSTALLED_APPS:
            self.is_guardian_supported = True

    def process_parent_class_list(self, parent_list, class_inst):
        if self.is_guardian_supported:
            try:
                from guardian.admin import GuardedModelAdmin
                if ModelAdmin in parent_list:
                    parent_list.remove(ModelAdmin)
                parent_list.append(GuardedModelAdmin)
            except ImportError:
                pass

    def process_admin_class_attr(self, admin_attr, class_inst):
        pass
