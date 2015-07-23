from django_extensions.admin import ForeignKeyAutocompleteAdmin
from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class ForeignKeyAutoCompleteFeature(AdminFeatureBase):
    def __init__(self):
        super(ForeignKeyAutoCompleteFeature, self).__init__()
        self.related_search_fields = {}

    def process_parent_class_list(self, parent_list, class_inst):
        parent_list.append(ForeignKeyAutocompleteAdmin)

    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr["related_search_fields"] = self.related_search_fields

    def set_related_search_fields(self, related_search_fields):
        self.related_search_fields = related_search_fields
