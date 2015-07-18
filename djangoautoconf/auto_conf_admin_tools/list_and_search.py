from django.db.models import DateTimeField
from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class ListAndSearch(AdminFeatureBase):
    def __init__(self):
        super(ListAndSearch, self).__init__()
        self.search_fields = []
        self.list_fields = []

    def set_list_and_search(self, list_display=None, search_fields=None):
        self.list_fields = list_display
        self.search_fields = search_fields

    def process_admin_class_attr(self, admin_attr, class_inst):
        if len(self.list_fields) == 0:
            admin_attr.update({"list_display": self.get_class_attributes(class_inst)})
        if len(self.search_fields) == 0:
            admin_attr.update({"search_fields": self.get_class_attributes(class_inst, [DateTimeField])})

    # noinspection PyMethodMayBeStatic
    def get_class_attributes(self, class_inst, exclude_field_types=[]):
        res = []
        try:
            for field in class_inst.__dict__['_meta'].fields:
                if type(field) in exclude_field_types:
                    continue
                res.append(field.name)
        except Exception, e:
            pass
        return res
