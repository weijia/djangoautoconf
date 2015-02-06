import copy
import inspect
from django.db.models import DateTimeField
from djangoautoconf.import_export_utils import get_import_export_resource


__author__ = 'q19420'
from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib import admin

if "guardian" in settings.INSTALLED_APPS:
    g_is_guardian_included = True
    from guardian.admin import GuardedModelAdmin


def register_admin_without_duplicated_register(class_inst, admin_class, admin_site=admin.site):
    try:
        if not (class_inst in admin_site._registry):
            admin_site.register(class_inst, admin_class)
    except Exception, e:
        if True:  # not (' is already registered' in e.message):
            print class_inst, admin_class
            import traceback
            traceback.print_exc()


class AdminRegister(object):
    def __init__(self, parent_admin_list=[]):
        super(AdminRegister, self).__init__()
        self.parent_admin_list = parent_admin_list
        self.base_model_admin = ModelAdmin
        self.admin_class_attributes = {}
        #self.is_import_export_supported = False

    def get_admin_class(self, class_instance):
        if self.admin_list is None:
            pass

    def get_valid_admin_class_with_list(self, class_inst):
        #print admin_list
        try:
            from import_export.admin import ImportExportActionModelAdmin
            self.base_model_admin = ImportExportActionModelAdmin
            resource_class = get_import_export_resource(class_inst)
            self.admin_class_attributes.update({
                "resource_class": resource_class
            })
        except ImportError:
            pass
        copied_admin_list = copy.copy(self.parent_admin_list)
        copied_admin_list.append(self.base_model_admin)
        #self.include_additional_admin_mixins(class_inst, copied_admin_list)
        #print ModelAdmin
        #print final_parents
        admin_class = type(class_inst.__name__ + "Admin", tuple(copied_admin_list), self.admin_class_attributes)
        return admin_class

    def register(self, class_inst, list_display=None, search_fields=None):
        self.admin_class_attributes = {}
        if not (list_display is None):
            self.admin_class_attributes["list_display"] = list_display
        if not (search_fields is None):
            self.admin_class_attributes["search_fields"] = search_fields
        admin_class = self.get_valid_admin_class_with_list(class_inst)
        register_admin_without_duplicated_register(class_inst, admin_class)

    def register_with_all_in_list_display(self, class_inst):
        self.admin_class_attributes["list_display"] = []
        self.admin_class_attributes["search_fields"] = []
        for field in class_inst.__dict__['_meta'].fields:
            if type(field) == DateTimeField:
                continue
            self.admin_class_attributes["list_display"].append(field.name)
            self.admin_class_attributes["search_fields"].append(field.name)
        admin_class = self.get_valid_admin_class_with_list(class_inst)
        register_admin_without_duplicated_register(class_inst, admin_class)

    def class_enumerator(self, module_instance, exclude_name_list):
        for name, obj in inspect.getmembers(module_instance):
            if inspect.isclass(obj):
                if name in exclude_name_list:
                    continue
                yield obj

    def register_all_model(self, module_instance, exclude_name_list=[]):
        """
        :param module_instance: mostly the models module
        :param exclude_name_list: class does not need to register or is already registered
        :param admin_class_list:
        :return: N/A
        """
        for class_instance in self.class_enumerator(module_instance, exclude_name_list):
            self.register_with_all_in_list_display(class_instance)

    # def include_additional_admin_mixins(self, class_instance, existing_list):
    #     try:
    #         from djangoautoconf.import_export_utils import get_import_export_admin_mixin
    #         existing_list.append(get_import_export_admin_mixin(class_instance))
    #         #from import_export.admin import ImportExportActionModelAdmin
    #         #existing_list.append(ImportExportActionModelAdmin)
    #     except ImportError:
    #         pass


