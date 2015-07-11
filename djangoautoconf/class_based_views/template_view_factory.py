import copy
import importlib

__author__ = 'weijia'


def force_list(item_or_list):
    if (type(item_or_list) is list) or (type(item_or_list) is tuple):
        return item_or_list
    else:
        return [item_or_list]


class TemplateViewFactory(object):

    def __init__(self):
        super(TemplateViewFactory, self).__init__()
        self.__parent_class_list = []
        self.__form_class = None
        self.__model_class = None
        self.__generic_parent_class = None
        self.__exclude = []
        self.__operation = ""

    def set_generic_template_view(self, operation):
        self.__operation = operation
        generic_module = importlib.import_module("django.views.generic")
        view_class_name = "%sView" % operation
        view_class = getattr(generic_module, view_class_name)
        # parent_class_tuple = (ajax_mixin, AjaxableFormContextUpdateMixin, view_class)
        # self.parent_class_list.append(view_class)
        # self.parent_class_list.append(view_class)
        self.__generic_parent_class = view_class

    def set_form_class(self, form_class):
        self.__form_class = form_class

    def set_model_class(self, model_class):
        self.__model_class = model_class

    def add_parent_class(self, parent_class_or_array):
        if (type(parent_class_or_array) is list) or (type(parent_class_or_array) is tuple):
            # parent_classes = copy.copy(parent_class_or_array)
            # parent_classes.append(self.parent_class_list[0])
            # self.parent_class_list = parent_classes
            self.__parent_class_list.extend(parent_class_or_array)
        else:
            # self.parent_class_list.insert(0, parent_class_or_array)
            self.__parent_class_list.append(parent_class_or_array)

    def set_exclude(self, exclude):
        self.__exclude = exclude

    def get_view(self):
        class_attributes = {
            # "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
            "template_name": "form_view_base_template.html",
            "submit_button_text": self.__operation,
            "success_url": "../"
        }
        if not (self.__model_class is None):
            class_attributes["model"] = self.__model_class

        if len(self.__exclude) > 0:
            class_attributes["exclude"] = self.__exclude

        if not (self.__form_class is None):
            class_attributes["form_class"] = self.__form_class

        create_view_class = type(self.__get_target_class_name(),
                                 self.__get_parent_class_tuple(),
                                 class_attributes)
        return create_view_class

    def __get_target_class_name(self):
        return "%s%s%s" % (self.__model_class.__name__, self.__operation, "View")

    def __get_parent_class_tuple(self):
        parent_classes = self.__parent_class_list
        parent_classes.append(self.__generic_parent_class)
        return tuple(parent_classes)
