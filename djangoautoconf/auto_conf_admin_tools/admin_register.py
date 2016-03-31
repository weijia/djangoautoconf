import copy
import types
from django.contrib.admin import ModelAdmin
from django.db import models
# from djangoautoconf.auto_conf_admin_tools.additional_attr import AdditionalAdminAttr
# from djangoautoconf.auto_conf_admin_tools.foreign_key_auto_complete import ForeignKeyAutoCompleteFeature
from djangoautoconf.auto_conf_admin_tools.guardian_feature import GuardianFeature
from djangoautoconf.auto_conf_admin_tools.import_export_feature import ImportExportFeature
from djangoautoconf.auto_conf_admin_tools.list_and_search import ListAndSearch
# from djangoautoconf.auto_conf_admin_tools.reversion_feature import ReversionFeature
from libtool.inspect_utils import class_enumerator
# from django.conf import settings
from django.contrib import admin


def register_admin_without_duplicated_register(class_inst, admin_class, admin_site=admin.site):
    # noinspection PyBroadException
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


# noinspection PyProtectedMember
def is_need_register(admin_site, class_inst):
    # if not is_inherit_from_model(class_inst):
    #     return False
    is_already_registered = class_inst in admin_site._registry
    is_can_register = True
    if hasattr(class_inst, "_meta"):
        if hasattr(class_inst._meta, "abstract"):
            is_can_register = not class_inst._meta.abstract
    return (not is_already_registered) and is_can_register


default_admin_site_list = [admin.site]

try:
    # noinspection PyUnresolvedReferences
    from normal_admin.admin import user_admin_site
    default_admin_site_list.append(user_admin_site)
except ImportError:
    pass


class AdminRegister(object):
    default_feature_list = [ListAndSearch, ImportExportFeature, GuardianFeature  # , ReversionFeature
                            ]

    def __init__(self, admin_site_list=default_admin_site_list, parent_admin_list=[]):
        super(AdminRegister, self).__init__()
        self.admin_features = []
        self.parent_admin_list = parent_admin_list
        # self.base_model_admin = ModelAdmin
        self.admin_class_attributes = {}

        for feature in self.default_feature_list:
            self.add_feature(feature())
        self.instant_admin_attr = {}
        self.admin_site_list = admin_site_list

    def get_valid_admin_class_with_list(self, class_inst, parent_admin=[]):

        copied_admin_list = copy.copy(self.parent_admin_list)
        copied_admin_list.extend(parent_admin)
        # copied_admin_list.append(self.base_model_admin)
        for feature in self.admin_features:
            feature.process_parent_class_list(copied_admin_list, class_inst)
            feature.process_admin_class_attr(self.admin_class_attributes, class_inst)

        # print ModelAdmin
        # print final_parents
        self.admin_class_attributes.update(self.instant_admin_attr)

        for attr in self.admin_class_attributes:
            new_method = self.admin_class_attributes[attr]
            if isinstance(new_method, types.FunctionType):
                self.admin_class_attributes[attr] = new_method

        if len(copied_admin_list) == 0:
            copied_admin_list = [ModelAdmin, ]
        admin_class = type(class_inst.__name__ + "Admin", tuple(copied_admin_list), self.admin_class_attributes)

        return admin_class

    def register_admin_without_duplicated_register(self, class_inst, admin_class):
        for admin_site in self.admin_site_list:
            register_admin_without_duplicated_register(class_inst, admin_class, admin_site)

    def register(self, class_inst, parent_admin=[]):
        admin_class = self.get_valid_admin_class_with_list(class_inst, parent_admin=[])
        self.register_admin_without_duplicated_register(class_inst, admin_class)

    def register_with_instant_fields(self, class_inst, instant_admin_attr):
        self.instant_admin_attr = instant_admin_attr
        self.register(class_inst)
        self.instant_admin_attr = {}

    def register_all_model(self, module_instance, exclude_name_list=[]):
        self.register_all_models(module_instance, exclude_name_list)

    def register_all_models(self, module_instance, exclude_name_list=[]):
        """
        :param module_instance: the module instance that containing models.Model inherited classes,
                mostly the models module
        :param exclude_name_list: class does not need to register or is already registered
        :return: N/A
        """
        for class_instance in class_enumerator(module_instance, exclude_name_list):
            if is_inherit_from_model(class_instance):
                self.register(class_instance)

    def add_feature(self, feature):
        self.admin_features.append(feature)
