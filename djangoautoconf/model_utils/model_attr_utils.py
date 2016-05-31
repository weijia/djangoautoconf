from django.db import models


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
