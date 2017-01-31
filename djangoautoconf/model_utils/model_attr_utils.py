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


def is_relation_field(field):
    if type(field) in get_relation_field_types():
        return True
    return False


enum_models = model_enumerator


def app_name_from_models_module(models_module):
    models_module.__name__.split(".")[0]


# Ref: http://stackoverflow.com/questions/2429074/how-can-i-get-access-to-a-django-model-field-verbose-name-dynamically
def get_verbose_name(model, field_name):
    # noinspection PyProtectedMember
    return model._meta.get_field_by_name(field_name)[0].verbose_name


class ModelsModule(object):
    def __init__(self):
        super(ModelsModule, self).__init__()
        self.models = models

    def enum_models(self, excluded_model_name):
        return model_enumerator(self.models, excluded_model_name)
