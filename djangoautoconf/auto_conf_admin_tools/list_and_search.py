from django.db.models import DateTimeField, ForeignKey
from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase
from django.db.models.fields.related import RelatedField

from djangoautoconf.model_utils.model_attr_utils import enum_model_fields

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
        # if len(self.list_fields) == 0:
        #     admin_attr.update({"list_display": self.get_class_attributes(class_inst)})
        if len(self.search_fields) == 0:
            admin_attr.update({"search_fields": self.get_contain_searchable_attr(
                class_inst)})

    def process_admin_class(self, admin_class, class_inst):
        if len(self.list_fields) == 0:
            list_display = list(getattr(admin_class, "list_display", []))
            if self.is_default_list_display(list_display):
                list_display = []
            field_list = self.get_class_attributes(class_inst)
            field_list.extend(list_display)
            setattr(admin_class, "list_display", tuple(field_list))

    # noinspection PyMethodMayBeStatic
    def is_default_list_display(self, list_display):
        return len(list_display) == 1 and list_display[0] == '__str__'

    # noinspection PyMethodMayBeStatic
    def get_class_attributes(self, class_inst, exclude_field_types=[]):
        res = []
        try:
            for field in enum_model_fields(class_inst):
                if type(field) in exclude_field_types:
                    continue
                try:
                    self.is_contain_searchable(field)
                    res.append(field.name)
                except TypeError:
                    pass
        except Exception as e:
            pass
        return res

    def get_contain_searchable_attr(self, class_inst):
        res = []
        try:
            for field in enum_model_fields(class_inst):
                if self.is_contain_searchable(field) and not (type(field) in [DateTimeField]):
                    res.append(field.name)
        except Exception as e:
            pass
        return res

    # noinspection PyMethodMayBeStatic
    def is_contain_searchable(self, field):
        try:
            field.get_prep_lookup("icontains", "test")
            if isinstance(field, RelatedField):
                return False
            return True
        except TypeError:
            return False
