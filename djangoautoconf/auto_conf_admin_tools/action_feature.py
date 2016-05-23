from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase

__author__ = 'weijia'


class ActionFeature(AdminFeatureBase):

    def __init__(self, name_and_act_dict):
        super(ActionFeature, self).__init__()
        self.name_and_act_dict = name_and_act_dict

    def process_parent_class_list(self, parent_list, class_inst):
        pass

    def process_admin_class_attr(self, admin_attr, class_inst):
        list_display = admin_attr.get("list_display", [])
        list_display.append()

        media_class = type("Media", tuple(), {
            "js": (
                '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
            )
        })
        admin_attr["Media"] = media_class
