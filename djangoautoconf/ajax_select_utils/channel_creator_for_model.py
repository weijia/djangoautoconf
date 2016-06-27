from ajax_select.registry import registry

from djangoautoconf.ajax_select_utils.ajax_select_channel_generator import register_channel
from djangoautoconf.model_utils.model_attr_utils import enum_model_fields, get_relation_field_types, \
    enum_model_fields_with_many_to_many, enum_model_many_to_many, model_enumerator
from ufs_tools.string_tools import class_name_to_low_case


def create_channels_for_related_fields_in_model(model_class):
    need_to_create_channel = []
    for field in enum_model_fields(model_class):
        if type(field) in get_relation_field_types():
            if field.related_model == 'self':
                need_to_create_channel.append(model_class)
            elif field.related_field.model not in need_to_create_channel:
                need_to_create_channel.append(field.related_field.model)

    for field in enum_model_many_to_many(model_class):
        if type(field) in get_relation_field_types():
            if field.related_model not in need_to_create_channel:
                need_to_create_channel.append(field.related_model)

    for field_model_class in need_to_create_channel:
        if class_name_to_low_case(field_model_class.__name__) not in registry._registry:
            register_channel(field_model_class)


def add_channel_for_models_in_module(models):
    for model_class in model_enumerator(models):
        create_channels_for_related_fields_in_model(model_class)
