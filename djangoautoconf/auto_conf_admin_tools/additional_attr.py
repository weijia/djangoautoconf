from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class AdditionalAdminAttr(AdminFeatureBase):

    def __init__(self):
        super(AdditionalAdminAttr, self).__init__()
        self.additional_attr_dict = {}

    def process_parent_class_list(self, parent_list, class_inst):
        pass

    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr.update(self.additional_attr_dict)

    def set_additional_attr(self, additional_attr_dict):
        self.additional_attr_dict = additional_attr_dict
