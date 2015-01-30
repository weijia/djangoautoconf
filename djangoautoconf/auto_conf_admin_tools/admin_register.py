import copy

__author__ = 'q19420'
from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib import admin

if "guardian" in settings.INSTALLED_APPS:
    g_is_guardian_included = True
    from guardian.admin import GuardedModelAdmin


class AdminRegister(object):
    def __init__(self, parent_admin_list=[]):
        super(AdminRegister, self).__init__()
        self.parent_admin_list = parent_admin_list
        self.base_model_admin = ModelAdmin
        self.admin_class_attributes = {}

    def get_admin_class(self, class_instance):
        if self.admin_list is None:
            pass

    def get_valid_admin_class_with_list(self, class_inst):
        #print admin_list
        copied_admin_list = copy.copy(self.parent_admin_list)
        copied_admin_list.append(self.base_model_admin)
        #print ModelAdmin
        #print final_parents
        admin_class = type(class_inst.__name__ + "Admin", tuple(copied_admin_list), self.admin_class_attributes)
        return admin_class

    def register(self, class_inst, list_display=None, search_fields=None):
        self.admin_class_attributes = {}
        if not (list_display is None):
            self.admin_class_attributes["list_display"] = list_display
        if not (search_fields is None):
            self.admin_class_attributes["list_display"] = search_fields
        admin_class = self.get_valid_admin_class_with_list(class_inst)
        admin.site.register(class_inst, admin_class)

    def register_with_all_in_list_display(self, class_inst):
        self.admin_class_attributes["list_display"] = []
        for field in class_inst.__dict__['_meta'].fields:
            self.admin_class_attributes["list_display"].append(field.name)
        admin_class = self.get_valid_admin_class_with_list(class_inst)
        admin.site.register(class_inst, admin_class)
        self.admin_class_attributes = {}