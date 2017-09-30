from django.core.management import BaseCommand

# from dj_catalog.models import TestingCatalog, FormalCatalog


def copy_objects(src_model, target_model):
    attr_list = get_model_attr_name_list(target_model)

    for field in enum_model_attr(target_model):
        if field.name not in attr_list:
            raise "Attribute does not exist"

    for obj in src_model.objects.all():
        item_dict = {}
        for attr in attr_list:
            item_dict[attr] = getattr(obj, attr)

        target_model.objects.get_or_create(**item_dict)


def get_model_attr_name_list(src_model):
    attr_list = []
    for field in enum_model_attr(src_model):
        attr_list.append(field.name)
    return attr_list


def enum_model_attr(src_model):
    return src_model.__dict__['_meta'].fields


# class ObjectCopier(BaseCommand):
#     def handle(self, *args, **options):
#         copy_object(TestingCatalog, FormalCatalog)
#
#
# Command = ObjectCopier
