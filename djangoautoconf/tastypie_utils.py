from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from req_with_auth import DjangoUserAuthentication


def create_tastypie_resource_class(class_inst):
    resource_class = type(class_inst.__name__ + "Resource", (ModelResource, ), {
        "Meta": type("Meta", (), {
            "queryset": class_inst.objects.all(),
            "resource_name": 'equip',
            "authentication": DjangoUserAuthentication(),
            "authorization": DjangoAuthorization(),
        })
    })
    return resource_class