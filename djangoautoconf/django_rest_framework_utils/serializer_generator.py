from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.serializers import ModelSerializer


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
