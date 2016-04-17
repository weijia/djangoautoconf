__author__ = 'weijia'


def get_model_perms(self, request):
    return {'add': True, 'change': True, 'delete': False}


def has_change_permission(self, request, obj=None):
    return True


class ModelWithFullPermissionFeature(object):
    def process_parent_class_list(self, parent_list, class_inst):
        pass

    # noinspection PyMethodMayBeStatic
    def process_admin_class_attr(self, admin_attr, class_inst):
        admin_attr["get_model_perms"] = get_model_perms
        admin_attr["has_change_permission"] = has_change_permission
        admin_attr["has_add_permission"] = has_change_permission

