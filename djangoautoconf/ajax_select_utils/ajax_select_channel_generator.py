from ajax_select import LookupChannel
from ajax_select.registry import registry
from django.conf.urls import url, include
from ajax_select import urls as ajax_select_urls
from django.db import models
from django.db.models import Q

from djangoautoconf.auto_conf_urls import add_to_root_url_pattern
from ufs_tools.string_tools import class_name_to_low_case

from djangoautoconf.model_utils.model_attr_utils import enum_model_fields

add_to_root_url_pattern(
    (url(r'^ajax_select/', include(ajax_select_urls)),)
)


class AutoLookupChannelBase(LookupChannel):
    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % unicode(item)

    def get_query(self, q, request):
        query = Q(pk__icontains=q)
        for field in self.dynamical_search_fields:
            param = {"%s__icontains" % field: q}
            query |= Q(**param)
        return self.model.objects.filter(query)[:10]


def get_fields_with_icontains_filter(model_class):
    text_fields = []
    for field in enum_model_fields(model_class):
        if type(field) in (models.TextField, models.CharField, models.IntegerField):
            text_fields.append(field.name)
    return text_fields


def register_channel(model_class, search_fields=()):
    """
    Register channel for model
    :param model_class: model to register channel for
    :param search_fields:
    :return:
    """
    if len(search_fields) == 0:
        search_fields = get_fields_with_icontains_filter(model_class)
    channel_class = type(model_class.__name__ + "LookupChannel",
                         (AutoLookupChannelBase,),
                         {"model": model_class,
                          "dynamical_search_fields": search_fields,
                          })
    channel_name = class_name_to_low_case(model_class.__name__)
    registry.register({channel_name: channel_class})
