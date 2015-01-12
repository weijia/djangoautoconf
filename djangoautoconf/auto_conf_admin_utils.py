import copy
import inspect
from django.conf import settings

if "guardian" in settings.INSTALLED_APPS:
    from guardian.admin import GuardedModelAdmin as SingleModelAdmin
else:
    from django.contrib.admin import ModelAdmin as SingleModelAdmin


#from django.contrib.admin import ModelAdmin
from django.contrib import admin
#The following not work with guardian?
#import xadmin as admin


def get_valid_admin_class(admin_class, class_inst):
    if admin_class is None:
        admin_class = type(class_inst.__name__ + "Admin", (SingleModelAdmin, ), {})
    return admin_class


def register_admin(admin_class, class_inst, admin_site=admin.site):
    try:
        if not (class_inst in admin_site._registry):
            admin_site.register(class_inst, admin_class)
    except Exception, e:
        if True:  # not (' is already registered' in e.message):
            print class_inst, admin_class
            import traceback
            traceback.print_exc()


def register_all_type_of_admin(admin_class, class_inst):
    register_admin(admin_class, class_inst)
    try:
        from normal_admin.admin import user_admin_site
        register_admin(admin_class, class_inst, user_admin_site)
    except ImportError:
        pass


def register_to_sys(class_inst, admin_class=None, is_normal_admin_needed=False):
    admin_class = get_valid_admin_class(admin_class, class_inst)
    if is_normal_admin_needed:
        register_all_type_of_admin(admin_class, class_inst)
    else:
        register_admin(admin_class, class_inst)


def get_valid_admin_class_with_list(admin_list, class_inst):
    #print admin_list
    copied_admin_list = copy.copy(admin_list)
    copied_admin_list.append(SingleModelAdmin)
    #print ModelAdmin
    #print final_parents
    admin_class = type(class_inst.__name__ + "Admin", tuple(copied_admin_list), {})
    return admin_class


def register_to_sys_with_admin_list(class_inst, admin_list=None, is_normal_admin_needed=False):
    """
    :param class_inst: model class
    :param admin_list: admin class
    :param is_normal_admin_needed: is normal admin registration needed
    :return:
    """
    if admin_list is None:
        admin_class = get_valid_admin_class_with_list([], class_inst)
    else:
        admin_class = get_valid_admin_class_with_list(admin_list, class_inst)
    if is_normal_admin_needed:
        register_all_type_of_admin(admin_class, class_inst)
    else:
        register_admin(admin_class, class_inst)


def register_all(class_list, admin_class_list=None):
    """
    :param class_list: list of class need to be registered to admin
    :param admin_class_list: parent of admin model class
    :return: no
    """
    for i in class_list:
        register_to_sys_with_admin_list(i, admin_class_list)


def register_all_in_module(module_instance, exclude_name_list=[], admin_class_list=None):
    """
    :param module_instance: mostly the models module
    :param exclude_name_list: class does not need to register or is already registered
    :param admin_class_list:
    :return:
    """
    class_list = []
    for name, obj in inspect.getmembers(module_instance):
        if inspect.isclass(obj):
            if obj.__name__ in exclude_name_list:
                continue
            class_list.append(obj)
    #print class_list, admin_class_list
    register_all(class_list, admin_class_list)