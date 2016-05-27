import inspect
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
    module = module = inspect.getmodule(caller_frame_record[0])
    module_name = module.__name__
    attr_dict = {'__module__': module_name}
    for field in class_inst.__dict__['_meta'].fields:
        attr_dict[field.name] = field
    duplicated_model_class = type(new_class_name, (models.Model, ), attr_dict)
    return duplicated_model_class
