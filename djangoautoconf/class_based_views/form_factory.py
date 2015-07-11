from django.forms import ModelForm
from djangoautoconf.class_based_views.template_view_factory import force_list

__author__ = 'weijia'


class ModelFormFactory(object):
    def __init__(self, model_class):
        super(ModelFormFactory, self).__init__()
        self.model_class = model_class
        self.exclude = []

    def set_exclude(self, exclude):
        self.exclude = force_list(exclude)

    def get_form_class(self):
        meta_class_attributes = {"model": self.model_class}

        if len(self.exclude) > 0:
            meta_class_attributes["exclude"] = self.exclude

        class_attributes = {
            "Meta": type("Meta", (), meta_class_attributes),
        }

        create_view_class = type(self.__get_target_class_name(),
                                 self.__get_parent_class_tuple(),
                                 class_attributes)
        return create_view_class

    def __get_target_class_name(self):
        return self.model_class.__name__ + "Form"

    def __get_parent_class_tuple(self):
        return (ModelForm,)