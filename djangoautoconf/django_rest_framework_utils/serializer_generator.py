from django.conf.urls import url, patterns
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.urlpatterns import format_suffix_patterns
from ufs_tools.string_tools import class_name_to_low_case

from djangoautoconf.model_utils.model_attr_utils import model_enumerator


class ModelSerializerWithUser(ModelSerializer):
    def save(self, **kwargs):
        user = None
        if "request" in self.context and self.context['request']:
            user = self.context['request'].user
        return super(ModelSerializerWithUser, self).save(user=user, **kwargs)


def get_serializer(class_inst, serializer_parent=[ModelSerializer]):
    meta_class = type("Meta", tuple(), {"model": class_inst})
    return type(class_inst.__name__ + "Serializer", tuple(serializer_parent),
                {"Meta": meta_class}
                )


def get_api_class(class_inst, suffix="List", parent=[ListCreateAPIView]):
    serializer = get_serializer(class_inst)
    api_class_name = class_inst.__name__ + suffix
    return get_api_class_from_serializer(class_inst, parent, serializer, api_class_name)


class ApiClassGenerator(object):
    def __init__(self, api_class_parent=[ListCreateAPIView], serializer_parent=[ModelSerializer]):
        super(ApiClassGenerator, self).__init__()
        self.api_class_parent = api_class_parent
        self.serializer_parent = serializer_parent
        self.suffix = "List"

    def get_api_class(self, class_inst):
        serializer = get_serializer(class_inst, self.serializer_parent)
        api_class_name = class_inst.__name__ + self.suffix
        res_class = get_api_class_from_serializer(class_inst, self.api_class_parent, serializer, api_class_name)
        return res_class


def get_api_class_from_serializer(class_inst, parent, serializer, api_class_name):
    return type(
        api_class_name,
        tuple(parent),
        {
            "queryset": class_inst.objects.all(),
            "serializer_class": serializer,
        }
    )


def get_create_api_class(class_inst):
    return get_api_class(class_inst)


def get_detail_api_class(class_inst):
    """
    Example: url(r'^checklist_list/(?P<pk>[0-9]+)/$', get_detail_api_class(ChecklistTreeItem).as_view()),
    :param class_inst:
    :return:
    """
    return get_api_class(class_inst, "Detail", [RetrieveUpdateDestroyAPIView])


class ModelProcessorBase(object):
    excluded_model_names = ('MPTTModel',)

    def __init__(self, url_patterns=None):
        self.url_list = []
        self.url_patterns = url_patterns

    def get_patterns(self, models):
        for model in model_enumerator(models, self.excluded_model_names):
            self.append_urls(model)
        p = patterns('', *self.url_list)
        return p

    def append_urls(self, model):
        self.url_list.append(self.get_url(model))

    def get_url(self, model):
        pass


class SerializerUrlGenerator(ModelProcessorBase):
    def append_urls(self, model):
        self.url_list.append(url(r'^rest_api/%s/$' % class_name_to_low_case(model.__name__),
                                 get_create_api_class(model).as_view()))
        self.url_list.append(url(r'^rest_api/%s/(?P<pk>[0-9]+)/$' % class_name_to_low_case(model.__name__),
                                 get_detail_api_class(model).as_view()))

    def add_rest_api_urls(self, models):
        if self.url_patterns is None:
            raise
        self.url_patterns += self.get_patterns(models)
        return format_suffix_patterns(self.url_patterns)