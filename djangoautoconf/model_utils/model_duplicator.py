import inspect
from django.db import models

from djangoautoconf.model_utils.model_attr_utils import is_relation_field
import copy
from django.db import models

__author__ = 'weijia'


def get_duplicated_model(class_inst, new_class_name):
    """
    Duplicate the model fields from class_inst to new_class_name, example:
    NewClass = get_duplicated_model(OldClass, "NewClass")
    :param class_inst:
    :param new_class_name:
    :return:
    """
    # Ref: http://www.cnblogs.com/Jerryshome/archive/2012/12/21/2827492.html
    # get caller stack frame
    # caller_frame = inspect.currentframe()
    caller_frame_record = inspect.stack()[1]

    # parse module name
    module = inspect.getmodule(caller_frame_record[0])
    return ModelDuplicator(module.__name__).get_duplicated_model(class_inst, new_class_name)


# Ref:
# https://stackoverflow.com/questions/12222003/copying-a-django-field-description-from-an-existing-model-to-a-new-one
def copy_field(f):
    fp = copy.copy(f)

    fp.creation_counter = models.Field.creation_counter
    models.Field.creation_counter += 1

    if hasattr(f, "model"):
        del fp.attname
        del fp.column
        del fp.model

        # you may set .name and .verbose_name to None here
    fp.db_index = f.db_index
    return fp


class ModelDuplicator(object):
    def __init__(self, module_name=None):
        super(ModelDuplicator, self).__init__()
        self.is_relation_field_needed = True
        if module_name is None:
            caller_frame_record = inspect.stack()[1]
            # parse module name
            module = inspect.getmodule(caller_frame_record[0])
            module_name = module.__name__
        self.module_name = module_name

    def get_duplicated_model(self, class_inst, new_class_name):
        """
        Duplicate the model fields from class_inst to new_class_name, example:
        NewClass = get_duplicated_model(OldClass, "NewClass")
        :param class_inst:
        :param new_class_name:
        :return:
        """
        # Ref: http://www.cnblogs.com/Jerryshome/archive/2012/12/21/2827492.html
        attr_dict = {'__module__': self.module_name}
        for field in class_inst.__dict__['_meta'].fields:
            if self.is_relation_field_needed:
                attr_dict[field.name] = copy_field(field)
            elif not is_relation_field(field):
                attr_dict[field.name] = copy_field(field)
        # duplicated_model_class = type("Meta", (), {"abstract": True})
        duplicated_model_class = type(new_class_name, (models.Model,), attr_dict)
        # The following codes are not working
        # if hasattr(class_inst, "__str__"):
        #     setattr(duplicated_model_class, "__str__", getattr(class_inst, "__str__"))
        # if hasattr(class_inst, "__str__"):
        #     str_func = getattr(class_inst, "__str__")
        #     duplicated_model_class.__str__ = str_func
        return duplicated_model_class
