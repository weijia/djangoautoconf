from import_export.admin import ImportExportMixin
from import_export import resources, fields

from djangoautoconf.model_utils.model_attr_utils import enum_model_fields


def get_import_export_resource(class_instance, resource_class_attributes=None, meta_class_attributes=None):
    """
    Generate the Resource class for a model. Resource class will like the following:
        class ModelClassNameAutoImportExportResource(resources.ModelResource):
            class Meta:
                model = ModelClass
    :param meta_class_attributes: additional Meta class attributes
    :param resource_class_attributes: additional resource class attributes
    :param class_instance: model class to generate the resource class for it
    :return:
    """
    attributes = {"model": class_instance}
    if meta_class_attributes:
        attributes.update(meta_class_attributes)
    resource_class_attributes = resource_class_attributes if resource_class_attributes is not None else {}
    resource_class_attributes.update({
        "Meta": type("Meta", (), attributes)
    })
    resource_class = type(class_instance.__name__ + "AutoImportExportResource", (resources.ModelResource, ),
                          resource_class_attributes)
    return resource_class


def get_import_export_admin_mixin_from_resource(class_instance, resource_class):
    admin_mixin_class = type(class_instance.__name__ + "AutoImportExportAdminMixin", (ImportExportMixin,), {
        "resource_class": resource_class
    })
    return admin_mixin_class


def get_import_export_admin_mixin(class_instance):
    resource_class = get_import_export_resource(class_instance)
    return get_import_export_admin_mixin_from_resource(class_instance, resource_class)


def get_import_export_resource_with_improved_title(class_instance):
    resource_class_attributes = get_resource_attributes(class_instance)
    return get_import_export_resource(class_instance, resource_class_attributes)


def get_resource_attributes(class_instance):
    resource_class_attributes = {}
    for field in enum_model_fields(class_instance):
        resource_class_attributes[field.name] = fields.Field(attribute=field.name, column_name=field.verbose_name)
    return resource_class_attributes


def get_import_export_admin_with_improved_title_mixin(class_instance):
    resource_class = get_import_export_resource_with_improved_title(class_instance)
    return get_import_export_admin_mixin_from_resource(class_instance, resource_class)


