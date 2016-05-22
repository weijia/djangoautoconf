from djangoautoconf.auto_conf_admin_tools.admin_feature_base import AdminFeatureBase
from tagging_app.tagging_app_utils import generate_html_attributes, get_tag_str

__author__ = 'weijia'


def gen_tags(self, obj):
    # on_click = "window.location='%d/run/?inline=1';" % obj.id
    # return '<input type="button" onclick="%s" value="Run" />' % on_click
    return '<ul class="tagged-item" %s>%s</ul>' % (generate_html_attributes(obj), get_tag_str(obj))


gen_tags.allow_tags = True
gen_tags.short_description = 'Tags'


class AdminTaggingFeature(AdminFeatureBase):
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
        attr = "list_display"
        gen_tags_list_name = "gen_tags"
        if hasattr(admin_class, attr) and hasattr(class_inst, "tags"):
            self.append_to_attr_tuple(admin_class, attr, [gen_tags_list_name])

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
            css.update({"all": 'jquery.qtip.min.css'})
            setattr(media_attr, css)

    # noinspection PyMethodMayBeStatic
    def append_to_attr_tuple(self, obj_instance, attribute_name, additional_value_list):
        tuple_attribute = list(getattr(obj_instance, attribute_name, []))
        tuple_attribute.extend(additional_value_list)
        setattr(obj_instance, attribute_name, tuple(tuple_attribute))
