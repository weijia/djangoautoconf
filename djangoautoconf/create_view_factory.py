from compat import JsonResponse
from django.views.generic import CreateView, UpdateView


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    success_url = "/"

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors#, status=400
                                )
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            title = ""
            if hasattr(self.object, "get_title"):
                title = self.object.get_title()
            data = {
                'pk': self.object.pk,
                'title': title
            }
            return JsonResponse(data)
        else:
            return response


def get_ajax_create_view_from_model(model_class):
    create_view_class = type(model_class.__name__ + "CreateView",
                             (AjaxableResponseMixin, CreateView), {
                                 # "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
                                 "model": model_class,
                             })
    return create_view_class


