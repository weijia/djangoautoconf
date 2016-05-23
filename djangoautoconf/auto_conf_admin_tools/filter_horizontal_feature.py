from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class FilterHorizontalFeature(AdminFeatureBase):
    """
    Use horizontal filter for foreign key attributes instead of multiple select box
    """
    def __init__(self, fields):
        """
        Init the feature
        :param fields: field set, for example: (username,)
        """
        super(FilterHorizontalFeature, self).__init__()
        self.filter_horizontal_fields = fields

    def set_filter_horizontal_fields(self, fields):
        self.filter_horizontal_fields = fields

    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr["filter_horizontal"] = self.filter_horizontal_fields
