from django.conf.urls import url, include
from tastypie import fields
from tastypie.api import NamespacedApi

try:
    from pieguard.authorization import GuardianAuthorization as AuthorizationClass
except ImportError:
    from tastypie.authorization import DjangoAuthorization as AuthorizationClass

from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import NamespacedModelResource

from djangoautoconf.model_utils.model_attr_utils import model_enumerator, enum_model_fields
from djangoautoconf.req_with_auth import DjangoUserAuthentication
from ufs_tools.string_tools import class_name_to_low_case


def create_tastypie_resource_class(class_inst, resource_name=None):
    if resource_name is None:
        resource_name = class_name_to_low_case(class_inst.__name__)
    meta_attributes = {"queryset": class_inst.objects.all(), "resource_name": resource_name,
                       "authentication": DjangoUserAuthentication(), "authorization": AuthorizationClass(),
                       "filtering": {}, "always_return_data": True}
    additional_resource_fields = {}
    for field in enum_model_fields(class_inst):

        if field.is_relation:
            if field.related_model is class_inst:
                additional_resource_fields[field.name] = fields.ForeignKey('self', field.name, null=True, blank=True)
            else:
                # Do not add filtering if it is foreign key, because we can not find the foreign key's resource
                continue
        meta_attributes["filtering"].update({field.name: ALL_WITH_RELATIONS})
    # The NamespacedModelResource used with NamespacedApi will ensure the namespace is added when calling reverse to
    # get the resource uri
    resource_attributes = {"Meta": type("Meta", (), meta_attributes)}
    resource_attributes.update(additional_resource_fields)
    resource_class = type(class_inst.__name__ + "AutoResource", (NamespacedModelResource,), resource_attributes)
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
            add_model_resource(model, v1_api)

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

    url_list.append(url(r'^api_domain_needed_signature/',
                        None))

    p = url_list
    return p


def add_model_resource(model, v1_api):
    resource = create_tastypie_resource(model)
    v1_api.register(resource)

