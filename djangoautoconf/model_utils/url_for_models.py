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
