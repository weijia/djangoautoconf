from django.contrib.admin import ModelAdmin

__author__ = 'weijia'


def queryset(self, request):
    qs = super(self.__class__, self).queryset(request)

    if request.user.is_superuser:
        return qs
    return qs.filter(user=request.user)


class FilterItemFeature(object):

    def process_parent_class_list(self, parent_list, class_inst):
        pass

    # noinspection PyMethodMayBeStatic
    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr["queryset"] = lambda self, request: \
            queryset(self, request)
