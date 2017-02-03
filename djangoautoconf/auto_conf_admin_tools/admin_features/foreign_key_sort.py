from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase


# Ref: http://stackoverflow.com/questions/8992865/django-admin-sort-foreign-key-field-list
def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == self.admin_feature_foreign_key_sort.sort_attribute:
        kwargs["queryset"] = db_field.related_model.objects.order_by(
            self.admin_feature_foreign_key_sort.sort_field_of_foreign_key)
    return super(self.__class__, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ForeignKeySortFeature(AdminFeatureBase):

    def __init__(self):
        super(ForeignKeySortFeature, self).__init__()
        self.model_class = None
        self.sort_attribute = None
        self.sort_field_of_foreign_key = None

    def process_admin_class_attr(self, admin_attr, class_inst):
        # super(ForeignKeySortFeature, self).process_admin_class_attr(admin_attr, class_inst)
        self.model_class = class_inst
        admin_attr["admin_feature_foreign_key_sort"] = self
        admin_attr["formfield_for_foreignkey"] = formfield_for_foreignkey

