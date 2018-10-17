import django
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

# from mezzanine.core.views import direct_to_template
from django.contrib.auth.decorators import login_required

admin.autodiscover()

# admin.site.login = login_required(admin.site.login)

# Must be defined before auto discover and urlpatterns var. So when there is root url
# injection, we first insert root url to this, then the last line will insert it to real urlpatterns
default_app_url_patterns = []

from djangoautoconf import auto_conf_urls

auto_conf_urls.autodiscover()

if django.VERSION[0] >= 2:
    from django.urls import path
    urlpatterns = [
        # Uncomment the next line to enable the admin:
        path('admin/', admin.site.urls),

    ]
else:
    urlpatterns = [
                           # Examples:
                           # url(r'^default_django_15_and_below/', include('default_django_15_and_below.foo.urls')),

                           # Uncomment the admin/doc line below to enable admin documentation:
                           url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                           # Uncomment the next line to enable the admin:
                           url(r'^admin/', include(admin.site.urls)),
                           # url(r'^', include('demo.urls')),
                           # url(r'^obj_sys/', include('obj_sys.urls')),
                           # url("^$", direct_to_template, {"template": "index.html"}, name="home"),
                           # url(r'^accounts/', include('userena.urls')),
                           ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += default_app_url_patterns
