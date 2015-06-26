from compat import JsonResponse
from django.views.generic import CreateView, UpdateView
from djangoautoconf.class_based_views.ajax_views import AjaxableResponseMixin


def get_ajax_create_view_from_model(model_class):
    create_view_class = type(model_class.__name__ + "CreateView",
                             (AjaxableResponseMixin, CreateView), {
                                 # "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
                                 "model": model_class,
                             })
    return create_view_class


