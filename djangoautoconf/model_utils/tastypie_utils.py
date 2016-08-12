from django.conf.urls import patterns, url, include
from tastypie.api import Api, NamespacedApi
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from tastypie.resources import ModelResource, NamespacedModelResource

from djangoautoconf.model_utils.model_attr_utils import model_enumerator
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
    # The NamespacedModelResource used with NamespacedApi will ensure the namespace is added when calling reverse to
    # get the resource uri
    resource_class = type(class_inst.__name__ + "AutoResource", (NamespacedModelResource,), {
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


def add_tastypie_for(urlpatterns, models, excluded_model_name=('MPTTModel',)):
    res_patterns = get_tastypie_urls(models, excluded_model_name)
    urlpatterns += res_patterns


def get_tastypie_urls(models, excluded_model_name=('MPTTModel',)):
    app_name = models.__name__.split(".")[0]
    # The urlconf_namespace and the above NamespacedModelResource will ensure the name space is added when
    # calling reverse to get the resource uri
    v1_api = NamespacedApi(api_name='v1', urlconf_namespace=app_name)
    url_list = []
    for model in model_enumerator(models, excluded_model_name):
        if hasattr(model, "objects"):
            resource = create_tastypie_resource(model)
            v1_api.register(resource)

    url_list.append(url(r'api/doc/',
                        include('tastypie_swagger.urls'),
                        kwargs={
                            "tastypie_api_module": v1_api,
                            "namespace": app_name,
                            "version": "1.0"}
                        ),
                    )
    url_list.append(url(r'^api/',
                        include(v1_api.urls)))

    p = patterns('', *url_list)
    return p
