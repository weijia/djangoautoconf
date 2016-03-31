from rest_framework import serializers
from rest_framework import generics


def get_serializer(class_inst):
    meta_class = type("Meta", tuple(), {"model": class_inst})
    return type(class_inst.__name__ + "Serializer", tuple([serializers.ModelSerializer]),
                {"Meta": meta_class}
                )


def get_api_class(class_inst, suffix="List", parent=[generics.ListCreateAPIView]):
    serializer = get_serializer(class_inst)
    return type(class_inst.__name__ + suffix, tuple(parent),
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
    return get_api_class(class_inst, "Detail", [generics.RetrieveUpdateDestroyAPIView])
