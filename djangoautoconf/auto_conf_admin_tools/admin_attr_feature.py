from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class AdminAttrFeature(AdminFeatureBase):

    def __init__(self, field_value_dict):
        """
        Init the fields and values
        :param field_value_dict: example: {"filter_horizontal": ("descriptions", )}
        """
        super(AdminAttrFeature, self).__init__()
        self.admin_attributes = field_value_dict

    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr.update(self.admin_attributes)
