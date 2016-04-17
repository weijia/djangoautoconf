from ajax_select import LookupChannel
from ajax_select.registry import registry
from django.conf.urls import url, include
from ajax_select import urls as ajax_select_urls
from django.db.models import Q

from djangoautoconf.auto_conf_urls import add_to_root_url_pattern
from libtool.string_tools import class_name_to_low_case

add_to_root_url_pattern(
    (url(r'^ajax_select/', include(ajax_select_urls)),)
)


class AutoLookupChannelBase(LookupChannel):
    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % unicode(item)

    def get_query(self, q, request):
        query = Q()
        for field in self.dynamical_search_fields:
            param = {"%s__icontains" % field: q}
            query |= Q(**param)
        return self.model.objects.filter(query)[:10]


def register_channel(model_inst, search_fields):
    channel_class = type(model_inst.__name__ + "LookupChannel",
                         (AutoLookupChannelBase,),
                         {"model": model_inst,
                          "dynamical_search_fields": search_fields,
                          })
    channel_name = class_name_to_low_case(model_inst.__name__)
    registry.register({channel_name: channel_class})
