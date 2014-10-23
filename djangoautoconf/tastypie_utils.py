from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from req_with_auth import DjangoUserAuthentication
import re


def class_name_to_low_case(class_name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_tastypie_resource_class(class_inst, resource_name=None):
    if resource_name is None:
        resource_name = class_name_to_low_case(class_inst.__name__)
    attributes = {"queryset": class_inst.objects.all(), "resource_name": resource_name,
                  "authentication": DjangoUserAuthentication(), "authorization": DjangoAuthorization(),
                  "filtering": {}}
    for field in class_inst.__dict__['_meta'].fields:
        attributes["filtering"].update({field.name: ALL})
    resource_class = type(class_inst.__name__ + "Resource", (ModelResource, ), {
        "Meta": type("Meta", (), attributes)
    })
    return resource_class


def create_tastypie_resource(class_inst):
    return create_tastypie_resource_class(class_inst)()