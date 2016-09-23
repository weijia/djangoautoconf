from django.db import models
from ufs_tools.inspect_utils import class_enumerator


def is_inherit_from_model(class_inst):
    if models.Model in class_inst.__bases__:
        return True
    for parent_class in class_inst.__bases__:
        if parent_class is object:
            continue
        return is_inherit_from_model(parent_class)
    return False


def enum_model_fields(class_inst):
    """
    ManyToManyField is not returned. If needed, use enum_model_fields_with_many_to_many instead
    :param class_inst:
    :return:
    """
    return class_inst.__dict__['_meta'].fields


def enum_model_fields_with_many_to_many(class_inst):
    for field in class_inst.__dict__['_meta'].fields:
        yield field
    for field in class_inst.__dict__['_meta'].many_to_many:
        yield field


def enum_model_many_to_many(class_inst):
    return class_inst.__dict__['_meta'].many_to_many


def get_relation_field_types():
    excluded_types = [models.ForeignKey, models.ManyToManyField]
    try:
        from mptt.models import TreeForeignKey
        excluded_types.append(TreeForeignKey)
    except ImportError:
        pass
    return excluded_types


def enum_relation_field(model_class):
    for field in enum_model_fields(model_class):
        if type(field) in get_relation_field_types():
            yield field


def model_enumerator(module_instance, exclude_name_list=None):
    exclude_name_list = exclude_name_list or []
    for class_instance in class_enumerator(module_instance, exclude_name_list):
        if is_inherit_from_model(class_instance):
            yield class_instance


enum_model = model_enumerator
