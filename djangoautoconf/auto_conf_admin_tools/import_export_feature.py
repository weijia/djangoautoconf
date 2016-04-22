from djangoautoconf.import_export_utils import get_import_export_resource
from django.conf import settings

__author__ = 'weijia'


class ImportExportFeature(object):

    def __init__(self):
        super(ImportExportFeature, self).__init__()
        self.is_import_export_supported = False

        if "import_export" in settings.INSTALLED_APPS:
            self.is_import_export_supported = True

    def process_parent_class_list(self, parent_list, class_inst):
        if self.is_import_export_supported:
            try:
                from import_export.admin import ImportExportActionModelAdmin
                parent_list.append(ImportExportActionModelAdmin)
            except ImportError:
                pass

    def process_admin_class_attr(self, admin_attr, class_inst):
        if self.is_import_export_supported:
            admin_attr.update({
                "resource_class": get_import_export_resource(class_inst)
            })
