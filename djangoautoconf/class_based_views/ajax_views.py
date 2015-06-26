from compat import JsonResponse

__author__ = 'weijia'


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    success_url = "/"

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors  # , status=400
                                )
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = self.get_result_dict()
            return JsonResponse(data)
        else:
            return response

    def get_result_dict(self):
        data = {
            'pk': self.object.pk,
        }
        return data


class AjaxableViewMixin(object):
    is_ajax_view = False
    action = "form"

    def get_template_names(self):
        if True:  # self.is_ajax_view:
            return ['modelview/object_%s.html' % self.action, ]
            # else:
            #     return ['modelview/object_%s.html' % self.action,]

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        context["base_template"] = ""
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )
