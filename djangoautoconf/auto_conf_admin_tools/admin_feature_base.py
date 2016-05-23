__author__ = 'weijia'


class AdminFeatureBase(object):

    def process_parent_class_list(self, parent_list, class_inst):
        """
        Used to add parent admin class to the list, all class in the list will be the admin class's parent
        :param parent_list:
        :param class_inst:
        :return:
        """
        pass

    def process_admin_class_attr(self, admin_attr, class_inst):
        """
        Used to add attributes to the actual admin class
        :param admin_attr:
        :param class_inst:
        :return:
        """
        pass
