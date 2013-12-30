#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import os
import sys
import base_settings
from utils import dump_attrs


class BaseDirNotExist(Exception):
    pass


class DjangoAutoConf(object):
    def __init__(self, default_settings_import_str, base_dir):
        if not os.path.exists(base_dir):
            raise BaseDirNotExist
        self.base_dir = base_dir
        self.default_settings_import_str = default_settings_import_str
        #Default keys is located at ../keys relative to universal_settings module
        self.key_dir = os.path.abspath(os.path.join(base_dir, "keys"))

    def set_base_dir(self, base_dir):
        self.base_dir = base_dir

    def set_key_dir(self, key_dir):
        self.key_dir = key_dir

    def configure(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoautoconf.base_settings")

        self.import_based_on_base_settings(self.default_settings_import_str)
        #dump_attrs(base_settings)
        self.import_based_on_base_settings("djangoautoconf.mysql_database")
        #dump_attrs(base_settings)

    def import_based_on_base_settings(self, module_import_path):
        #######
        # Inject attributes to builtin and import all other modules
        # Ref: http://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function
        self.init_builtin()
        self.inject_attr()
        new_base_settings = importlib.import_module(module_import_path)
        self.remove_attr()
        update_base_settings(new_base_settings)

    def inject_attr(self):
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            if hasattr(self.builtin, attr):
                raise "Attribute already exists"
            self.builtin[attr] = value

    def remove_attr(self):
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            del self.builtin[attr]

    def init_builtin(self):
        try:
            self.__dict__['builtin'] = sys.modules['__builtin__'].__dict__
        except KeyError:
            self.__dict__['builtin'] = sys.modules['builtins'].__dict__


def update_base_settings(new_base_settings):
    for attr in dir(new_base_settings):
        if attr != attr.upper():
            continue
        value = getattr(new_base_settings, attr)
        setattr(base_settings, attr, value)