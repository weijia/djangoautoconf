from django.conf.urls import patterns
import models
from djangoautoconf.model_utils.url_for_models import add_all_urls


urlpatterns = patterns('',
                       )

add_all_urls(urlpatterns, models)
