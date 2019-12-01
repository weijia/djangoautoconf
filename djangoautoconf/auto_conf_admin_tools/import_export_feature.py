from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase
from django.conf import settings

from djangoautoconf.model_utils.import_export_utils import get_import_export_admin_mixin, \
    get_import_export_admin_with_improved_title_mixin

__author__ = 'weijia'


class ImportExportFeature(AdminFeatureBase):

    def __init__(self):
        super(ImportExportFeature, self).__init__()
        self.is_import_export_supported = False

        if "import_export" in settings.INSTALLED_APPS:
            self.is_import_export_supported = True

    def process_parent_class_list(self, parent_list, class_inst):
        if self.is_import_export_supported:
            try:
                # from import_export.admin import ImportExportActionModelAdmin
                if hasattr(class_inst, "use_verbose_as_export_title"):
                    parent_list.append(get_import_export_admin_with_improved_title_mixin(class_inst))
                else:
                    parent_list.append(get_import_export_admin_mixin(class_inst))
            except ImportError:
                pass

    def process_admin_class_attr(self, admin_attr, class_inst):
        # if self.is_import_export_supported:
        #     admin_attr.update({
        #         "resource_class": get_import_export_resource(class_inst)
        #     })
        pass

