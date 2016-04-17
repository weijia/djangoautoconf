import copy

from django.db.models import ForeignKey, ManyToManyField
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from mptt.fields import TreeForeignKey

from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class ForeignKeyAutoCompleteFeature(AdminFeatureBase):
    """
    !!!This field is not compatible to django-ajax-selects!!!
    """
    def __init__(self):
        super(ForeignKeyAutoCompleteFeature, self).__init__()
        self.related_search_fields = {}
        self.search_field_by_model = None

    def process_parent_class_list(self, parent_list, class_inst):
        parent_list.append(ForeignKeyAutocompleteAdmin)

    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr["related_search_fields"] = copy.copy(self.related_search_fields)
        if not (self.search_field_by_model is None):
            for field in class_inst.__dict__['_meta'].fields:
                if (type(field) is ForeignKey) or (type(field) is TreeForeignKey):
                    if field.rel.to in self.search_field_by_model.keys():
                        admin_attr["related_search_fields"][field.name] = self.search_field_by_model[field.rel.to]

    def set_related_search_fields(self, related_search_fields):
        """
        Set the related search field, check django-extensions/ForeignKeyAutocompleteAdmin for detail
        :param related_search_fields:
            {
               'user': ('first_name', 'email'),
            }
        :return:
        """
        self.related_search_fields = related_search_fields

    def set_search_field_by_model(self, search_field_by_model):
        """
        Set common model search field
        :param search_field_by_model:
            {
               User: ('first_name', 'email'),
            }
        :return:
        """
        self.search_field_by_model = search_field_by_model
