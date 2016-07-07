from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import DetailView


def all_valid(formsets):
    """Returns true if every formset in formsets is valid."""
    valid = True
    for formset in formsets:
        if not formset.is_valid():
            valid = False
    return valid


class DetailWithInlineView(DetailView):
    template_name = "detail_with_inline_view.html"
    inlines = []
    model = None
    success_url = ""

    def get_context_data(self, **kwargs):
        context = super(DetailWithInlineView, self).get_context_data(**kwargs)
        inlines = self.construct_inlines()
        context.update({"inlines": inlines})
        return context

    def get_inlines(self):
        """
        Returns the inline formset classes
        """
        return self.inlines

    def forms_valid(self, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        for formset in inlines:
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, inlines):
        """
        If the form or formsets are invalid, re-render the context data with the
        data-filled form and formsets and errors.
        """
        return self.render_to_response(self.get_context_data(inlines=inlines))

    def construct_inlines(self):
        """
        Returns the inline formset instances
        """
        inline_formsets = []
        for inline_class in self.get_inlines():
            inline_instance = inline_class(self.model, self.request, self.object, self.kwargs, self)
            inline_formset = inline_instance.construct_formset()
            inline_formsets.append(inline_formset)
        return inline_formsets

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form and formset instances with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object()
        self.get_context_data()
        inlines = self.construct_inlines()

        if all_valid(inlines):
            return self.forms_valid(inlines)
        return self.forms_invalid(inlines)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url
