import copy
from django.db import models
from djangoautoconf.auto_conf_admin_tools.additional_attr import AdditionalAdminAttr
from djangoautoconf.auto_conf_admin_tools.foreign_key_auto_complete import ForeignKeyAutoCompleteFeature
from djangoautoconf.auto_conf_admin_tools.import_export_feature import ImportExportFeature
from djangoautoconf.auto_conf_admin_tools.list_and_search import ListAndSearch
from libtool.inspect_utils import class_enumerator
from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib import admin


def register_admin_without_duplicated_register(class_inst, admin_class, admin_site=admin.site):
    try:
        if is_need_register(admin_site, class_inst):
            admin_site.register(class_inst, admin_class)
    except Exception, e:
        if True:  # not (' is already registered' in e.message):
            print class_inst, admin_class
            import traceback
            traceback.print_exc()


def is_inherit_from_model(class_inst):
    if models.Model in class_inst.__bases__:
        return True
    for parent_class in class_inst.__bases__:
        if parent_class is object:
            continue
        return is_inherit_from_model(parent_class)
    return False


def is_need_register(admin_site, class_inst):
    # if not is_inherit_from_model(class_inst):
    #     return False
    is_already_registered = class_inst in admin_site._registry
    is_can_register = True
    if hasattr(class_inst, "_meta"):
        if hasattr(class_inst._meta, "abstract"):
            is_can_register = not class_inst._meta.abstract
    return (not is_already_registered) and is_can_register


class AdminRegister(object):
    def __init__(self, parent_admin_list=[], admin_feature_list=[]):
        super(AdminRegister, self).__init__()
        self.admin_features = []
        self.parent_admin_list = parent_admin_list
        self.base_model_admin = ModelAdmin
        self.admin_class_attributes = {}
        # self.is_import_export_supported = False
        self.admin_site_list = [admin.site, ]
        try:
            from normal_admin.admin import user_admin_site
            self.admin_site_list.append(user_admin_site)
        except ImportError:
            pass

        self.list_search_feature = ListAndSearch()
        self.admin_features.append(self.list_search_feature)
        self.import_export_feature = ImportExportFeature()
        self.add_feature(self.import_export_feature)

    def get_valid_admin_class_with_list(self, class_inst):
        # print admin_list

        if "guardian" in settings.INSTALLED_APPS:
            # g_is_guardian_included = True
            try:
                from guardian.admin import GuardedModelAdmin
                self.base_model_admin = GuardedModelAdmin
            except ImportError:
                pass

        copied_admin_list = copy.copy(self.parent_admin_list)
        copied_admin_list.append(self.base_model_admin)
        for feature in self.admin_features:
            feature.process_parent_class_list(copied_admin_list, class_inst)
            feature.process_admin_class_attr(self.admin_class_attributes, class_inst)

        # print ModelAdmin
        # print final_parents

        admin_class = type(class_inst.__name__ + "Admin", tuple(copied_admin_list), self.admin_class_attributes)
        return admin_class

    def register_admin_without_duplicated_register(self, class_inst, admin_class):
        for admin_site in self.admin_site_list:
            register_admin_without_duplicated_register(class_inst, admin_class, admin_site)

    def register(self, class_inst):
        admin_class = self.get_valid_admin_class_with_list(class_inst)
        self.register_admin_without_duplicated_register(class_inst, admin_class)

    # def register_all_with_additional_attributes(self, class_inst, admin_class_attributes={}):
    #     additional_attr_feature = AdditionalAdminAttr()
    #     additional_attr_feature.set_additional_attr(admin_class_attributes)
    #     self.admin_features.append(additional_attr_feature)
    #     self.register(class_inst)
    #
    # def register_with_all_in_list_display(self, class_inst):
    #     self.register(class_inst)

    def register_all_model(self, module_instance, exclude_name_list=[]):
        self.register_all_models(module_instance, exclude_name_list)

    def register_all_models(self, module_instance, exclude_name_list=[]):
        """
        :param module_instance: mostly the models module
        :param exclude_name_list: class does not need to register or is already registered
        :param admin_class_list:
        :return: N/A
        """
        for class_instance in class_enumerator(module_instance, exclude_name_list):
            if is_inherit_from_model(class_instance):
                self.register(class_instance)

    def add_feature(self, feature):
        self.admin_features.append(feature)

    # def include_additional_admin_mixins(self, class_instance, existing_list):
    #     try:
    #         from djangoautoconf.import_export_utils import get_import_export_admin_mixin
    #         existing_list.append(get_import_export_admin_mixin(class_instance))
    #         #from import_export.admin import ImportExportActionModelAdmin
    #         #existing_list.append(ImportExportActionModelAdmin)
    #     except ImportError:
    #         pass


