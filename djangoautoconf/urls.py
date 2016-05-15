from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

# from mezzanine.core.views import direct_to_template

admin.autodiscover()

# Must be defined before auto discover and urlpatterns var. So when there is root url
# injection, we first insert root url to this, then the last line will insert it to real urlpatterns
default_app_url_patterns = []

from djangoautoconf import auto_conf_urls

auto_conf_urls.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^default_django_15_and_below/', include('default_django_15_and_below.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^', include('demo.urls')),
                       # url(r'^obj_sys/', include('obj_sys.urls')),
                       # url("^$", direct_to_template, {"template": "index.html"}, name="home"),
                       )

urlpatterns += default_app_url_patterns
