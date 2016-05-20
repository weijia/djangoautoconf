from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from djangoautoconf.req_with_auth import DjangoUserAuthentication
from ufs_tools.string_tools import class_name_to_low_case


def create_tastypie_resource_class(class_inst, resource_name=None):
    if resource_name is None:
        resource_name = class_name_to_low_case(class_inst.__name__)
    attributes = {"queryset": class_inst.objects.all(), "resource_name": resource_name,
                  "authentication": DjangoUserAuthentication(), "authorization": DjangoAuthorization(),
                  "filtering": {}, "always_return_data": True}
    for field in class_inst.__dict__['_meta'].fields:
        attributes["filtering"].update({field.name: ALL})
    resource_class = type(class_inst.__name__ + "AutoResource", (ModelResource, ), {
        "Meta": type("Meta", (), attributes)
    })
    return resource_class


def create_tastypie_resource(class_inst):
    """
    Usage: url(r'^api/', include(create_tastypie_resource(UfsObjFileMapping).urls)),
    Access url: api/ufs_obj_file_mapping/?format=json
    :param class_inst:
    :return:
    """
    return create_tastypie_resource_class(class_inst)()
