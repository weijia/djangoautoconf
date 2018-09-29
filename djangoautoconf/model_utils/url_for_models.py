from ufs_tools.string_tools import class_name_to_low_case

from djangoautoconf.ajax_select_utils.channel_creator_for_model import add_channel_for_models_in_module
from djangoautoconf.django_rest_framework_utils.serializer_generator import SerializerUrlGenerator
from djangoautoconf.model_utils.tastypie_utils import get_tastypie_urls


def add_all_urls(urlpatterns, models):
    urlpatterns += get_tastypie_urls(models)
    try:
        from django_auto_filter.filter_for_models import get_filter_urls
        urlpatterns += get_filter_urls(models)
    except ImportError:
        get_filter_urls = None
        pass
    urlpatterns = SerializerUrlGenerator(urlpatterns).add_rest_api_urls(models)
    add_channel_for_models_in_module(models)
    return urlpatterns


# noinspection PyProtectedMember
def get_model_app(model_class):
    # app_folder = os.path.dirname(get_folder(model_class.__file__))
    # name = os.path.basename(app_folder)
    return model_class._meta.app_label
    # return name


def get_rest_api_url(model_class):
    rest_api_url = "/%s/rest_api/%s/" % (get_model_app(model_class), class_name_to_low_case(model_class.__name__))
    return rest_api_url


def get_tastypie_api_url(model_class, app_name=None):
    app_name = app_name or get_model_app(model_class)
    rest_api_url = "/%s/api/v1/%s/" % (app_name, class_name_to_low_case(model_class.__name__))
    return rest_api_url



