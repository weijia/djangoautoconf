from django.db.models import DateTimeField, ForeignKey
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
            admin_attr.update({"search_fields": self.get_contain_searchable_attr(
                class_inst)})

    # noinspection PyMethodMayBeStatic
    def get_class_attributes(self, class_inst, exclude_field_types=[]):
        res = []
        try:
            for field in self.enum_model_fields(class_inst):
                if type(field) in exclude_field_types:
                    continue
                try:
                    self.is_contain_searchable(field)
                    res.append(field.name)
                except TypeError:
                    pass
        except Exception, e:
            pass
        return res

    def get_contain_searchable_attr(self, class_inst):
        res = []
        try:
            for field in self.enum_model_fields(class_inst):
                if self.is_contain_searchable(field) and not (type(field) in [DateTimeField]):
                    res.append(field.name)
        except Exception, e:
            pass
        return res

    # noinspection PyMethodMayBeStatic
    def is_contain_searchable(self, field):
        try:
            field.get_prep_lookup("icontains", "test")
            return True
        except TypeError:
            return False

    # noinspection PyMethodMayBeStatic
    def enum_model_fields(self, class_inst):
        return class_inst.__dict__['_meta'].fields
