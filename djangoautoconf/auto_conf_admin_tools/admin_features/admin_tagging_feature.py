from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase
from tagging_app.tagging_app_utils import generate_html_attributes, get_tag_str

__author__ = 'weijia'


def gen_tags(self, obj):
    # on_click = "window.location='%d/run/?inline=1';" % obj.id
    # return '<input type="button" onclick="%s" value="Run" />' % on_click
    tag_str = get_tag_str(obj)
    if tag_str == "":
        tag_str = "no tag"
    return '<ul class="tagged-item" %s>%s</ul>' % (generate_html_attributes(obj), tag_str)


gen_tags.allow_tags = True
gen_tags.short_description = 'Tags'


class AdminTaggingFeature(AdminFeatureBase):
    def __init__(self):
        self.insert_position = 1
        self.insert_field = "list_display"

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

    # noinspection PyMethodMayBeStatic
    def process_admin_class(self, admin_class, class_inst):
        gen_tags_list_name = "gen_tags"
        if hasattr(admin_class, self.insert_field) and hasattr(class_inst, "tags"):
            self.insert_tag_field(admin_class)

            setattr(admin_class, gen_tags_list_name, gen_tags)

            if not hasattr(admin_class, "Media"):
                setattr(admin_class, "Media", type("Media", tuple(), {}))
            media_attr = getattr(admin_class, "Media")
            self.append_to_attr_tuple(media_attr, "js", (
                # '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
                # 'jquery.qtip.min.css',
                'js/jquery-ui.js',
                'jquery.qtip.min.js',
                'js/tagging_ajax.js',
                'js/tagging_app.js',
                'js/tag_app_init.js',
                # 'obj_sys/js/jQuery-Tags-Input/src/jquery.tagsinput.js',
            ))
            css = getattr(media_attr, "css", {})
            css.update({"all": ('jquery.qtip.min.css',)})
            setattr(media_attr, "css", css)

    # noinspection PyMethodMayBeStatic
    def append_to_attr_tuple(self, obj_instance, attribute_name, additional_value_list):
        tuple_attribute = list(getattr(obj_instance, attribute_name, []))
        tuple_attribute.extend(additional_value_list)
        setattr(obj_instance, attribute_name, tuple(tuple_attribute))

    # noinspection PyMethodMayBeStatic
    def insert_tag_field(self, obj_instance):
        list_display = list(getattr(obj_instance, self.insert_field, []))
        list_display.insert(self.insert_position, "gen_tags")
        setattr(obj_instance, self.insert_field, tuple(list_display))
