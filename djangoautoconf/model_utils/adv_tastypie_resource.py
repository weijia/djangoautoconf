from tastypie.api import NamespacedApi
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.resources import NamespacedModelResource
from django.conf.urls import url, include
from djangoautoconf.model_utils.model_attr_utils import enum_model_fields, enum_models, \
    enum_model_fields_with_many_to_many, ModelsModule, app_name_from_models_module
from djangoautoconf.req_with_auth import DjangoUserAuthentication
from ufs_tools.string_tools import class_name_to_low_case

try:
    from pieguard.authorization import GuardianAuthorization as AuthorizationClass
except ImportError:
    from tastypie.authorization import DjangoAuthorization as AuthorizationClass


class TastypieResourceGenerator(object):
    def __init__(self, registry, model):
        super(TastypieResourceGenerator, self).__init__()
        self.registry = registry
        self.model = model
        self.additional_resource_class_attr = {}
        resource_name = class_name_to_low_case(self.model.__name__)
        self.meta_attr = {"queryset": self.model.objects.all(), "resource_name": resource_name,
                          "authentication": DjangoUserAuthentication(), "authorization": AuthorizationClass(),
                          "filtering": {}, "always_return_data": True}

    def create_resource_class(self):
        # The NamespacedModelResource used with NamespacedApi will ensure the namespace is added when calling reverse to
        resource_class = type(self.model.__name__ + "AutoResource", (NamespacedModelResource,),
                              self._get_resource_attr())
        return resource_class

    def _get_resource_attr(self):
        self._update_resource_attributes()
        resource_attributes = {"Meta": type("Meta", (), self.meta_attr)}
        resource_attributes.update(self.additional_resource_class_attr)
        return resource_attributes

    def _update_resource_attributes(self):
        for field in enum_model_fields_with_many_to_many(self.model):
            self.meta_attr["filtering"].update({field.name: ALL_WITH_RELATIONS})
            is_include_full = True
            if field.is_relation:
                if field.related_model is self.model:
                    target_resource = 'self'
                    is_include_full = False
                elif self.registry.is_resource_exists(field.related_model):
                    target_resource = self.registry.get_resource_class(field.related_model)
                else:
                    continue
                if field.many_to_many:
                    attribute_class = fields.ToManyField
                else:
                    attribute_class = fields.ForeignKey

                self.additional_resource_class_attr[field.name] = attribute_class(
                    target_resource, field.name, null=True, blank=True, full=is_include_full)


class AdvTastypieResourceGenerator(object):
    def __init__(self):
        self.registry = {}

    def get_resource(self, model):
        return self.get_resource_class(model)()

    def is_resource_exists(self, model):
        return model in self.registry

    def get_resource_class(self, model):
        if model not in self.registry:
            self.registry[model] = self.create_resource_class(model)
        return self.registry[model]

    def create_resource_class(self, model):
        t = TastypieResourceGenerator(self, model)
        return t.create_resource_class()


class TastypieApiGenerator(object):
    def __init__(self, namespace):
        """
        Create api
        :param namespace: namespace should be the application name, as we'll set applications to use application name
         as the url conf namespace
        """
        super(TastypieApiGenerator, self).__init__()
        self.generator = AdvTastypieResourceGenerator()
        # The urlconf_namespace and the above NamespacedModelResource will ensure the name space is added when
        # calling reverse to get the resource uri
        self.v1_api = NamespacedApi(api_name='v1', urlconf_namespace=namespace)

    def get_model_api_url_list(self):
        url_list = [url(r'^api/',
                        include(self.v1_api.urls))]
        return url_list

    def register_all(self, models):
        for model in enum_models(models):
            if hasattr(model, "objects"):
                self.register_resource_for_model(model)

    def register_resource_for_model(self, model):
        resource = self.generator.get_resource(model)
        self.v1_api.register(resource)


class TastypieApiUrlGenerator(object):
    def __init__(self, models):
        self.models = models
        self.generator = TastypieApiGenerator(app_name_from_models_module(models))

    def get_model_api_url_list(self):
        self.generator.register_all(self.models)
        return self.generator.get_model_api_url_list()
