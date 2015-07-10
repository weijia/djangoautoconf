import importlib
# from compat import JsonResponse
# from django.views.generic import CreateView, UpdateView
from djangoautoconf.class_based_views.ajax_views import AjaxableResponseMixin


# def get_ajax_create_view_from_model(model_class):
#     create_view_class = type(model_class.__name__ + "CreateView",
#                              (AjaxableResponseMixin, CreateView), {
#                                  # "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
#                                  "model": model_class,
#                                  "template_name": "form_view_base_template.html",
#                              })
#     return create_view_class


class AjaxableFormContextUpdateMixin(object):
    submit_button_text = "Update"
    ajax_form_id = "UpdateForm"

    def get_context_data(self, **kwargs):
        # super_class = super(self.__class__, self)
        # super_class.remove(ContextUpdateMixin)
        for class_instance in self.__class__.__bases__:
            if class_instance is AjaxableFormContextUpdateMixin or not hasattr(class_instance, "get_context_data"):
                continue
            context = class_instance.get_context_data(self, **kwargs)
        context["submit_button_text"] = self.submit_button_text
        context["ajax_form_id"] = self.ajax_form_id
        return context


def create_ajaxable_view_from_model_inherit_parent_class(model_class, parent_class_list, operation="Create"):
    """
    :param model_class: the django model class
    :param operation: "Create" or "Update"
    :param ajax_mixin: user may pass a sub class of AjaxableResponseMixin to put more info in the ajax response
    :return: dynamically generated class based view. The instance of the view class has as_view method.
    """
    generic_module = importlib.import_module("django.views.generic")
    view_class_name = "%sView" % operation
    view_class = getattr(generic_module, view_class_name)
    # parent_class_tuple = (ajax_mixin, AjaxableFormContextUpdateMixin, view_class)
    parent_class_list.append(view_class)
    create_view_class = type("%s%s%s" % (model_class.__name__, operation, "View"),
                             tuple(parent_class_list), {
                                 # "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
                                 "model": model_class,
                                 "template_name": "form_view_base_template.html",
                                 "submit_button_text": operation,
                                 "success_url": "../"
                             })
    return create_view_class


def create_ajaxable_view_from_model(model_class, operation="Create", ajax_mixin=AjaxableResponseMixin):
    # """
    # :param model_class: the django model class
    # :param operation: "Create" or "Update"
    # :param ajax_mixin: user may pass a sub class of AjaxableResponseMixin to put more info in the ajax response
    # :return: dynamically generated class based view. The instance of the view class has as_view method.
    # """
    # generic_module = importlib.import_module("django.views.generic")
    # view_class_name = "%sView" % operation
    # view_class = getattr(generic_module, view_class_name)
    # create_view_class = type("%s%s%s" % (model_class.__name__, operation, "View"),
    #                          (ajax_mixin, AjaxableFormContextUpdateMixin, view_class), {
    #                              # "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
    #                              "model": model_class,
    #                              "template_name": "form_view_base_template.html",
    #                              "submit_button_text": operation,
    #                          })
    # return create_view_class
    return create_ajaxable_view_from_model_inherit_parent_class(model_class, [ajax_mixin, AjaxableFormContextUpdateMixin])
