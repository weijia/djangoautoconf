from guardian.admin import GuardedModelAdmin

#from django.contrib import admin
import xadmin as admin


def register_to_sys(class_inst, admin_class = None):
    if admin_class is None:
        admin_class = type(class_inst.__name__+"Admin", (GuardedModelAdmin, ), {})
    try:
        admin.site.register(class_inst, admin_class)
    except:
        pass
    try:
        from normal_admin.admin import user_admin_site
        user_admin_site.register(class_inst, admin_class)
    except:
        pass
    #register(class_inst)


def register_all(class_list):
    for i in class_list:
        register_to_sys(i)