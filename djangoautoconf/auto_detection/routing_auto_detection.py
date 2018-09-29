from importlib import import_module

from djangoautoconf.auto_conf_urls import enum_app_names
from djangoautoconf.auto_conf_utils import is_at_least_one_sub_filesystem_item_exists, get_module_path
from ufs_tools.short_decorator.ignore_exception import ignore_exc_with_result


def autodiscover():
    from django.conf import settings
    routing_holder = settings.CHANNEL_LAYERS["default"]["ROUTING"]
    routing_module = ".".join(routing_holder.split(".")[0:-1])
    root_url = import_module(routing_module)
    root_default_channel_routing = root_url.default_channel_routing

    for app in enum_app_names():
        if app == "channels":
            continue
        mod = import_module(app)
        if is_at_least_one_sub_filesystem_item_exists(get_module_path(mod), ["routing.py"]):
            routing_module_name = "%s.routing" % app

            routing_settings = get_routing_settings(routing_module_name)
            root_default_channel_routing.extend(routing_settings)


@ignore_exc_with_result(exception_result=[], is_notification_needed=True)
def get_routing_settings(routing_module_name):
    routing_module = import_module(routing_module_name)
    routing_settings = routing_module.channel_routing
    return routing_settings
