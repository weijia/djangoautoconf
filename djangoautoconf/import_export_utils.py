from import_export.admin import ImportExportMixin

__author__ = 'q19420'
from import_export import resources


def get_import_export_resource(class_instance):
    attributes = {"model": class_instance}
    resource_class = type(class_instance.__name__ + "AutoImportExportResource", (resources.ModelResource, ), {
        "Meta": type("Meta", (), attributes)
    })
    return resource_class


def get_import_export_admin_mixin(class_instance):
    resource_class = get_import_export_resource(class_instance)
    admin_mixin_class = type(class_instance.__name__ + "AutoImportExportAdminMixin", (ImportExportMixin,), {
        "resource_class": resource_class
    })
    return admin_mixin_class