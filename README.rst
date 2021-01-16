===============================
Django AutoConf
===============================

.. image:: https://badge.fury.io/py/djangoautoconf.png
    :target: http://badge.fury.io/py/djangoautoconf
    
.. image:: https://travis-ci.org/weijia/djangoautoconf.png?branch=master
        :target: https://travis-ci.org/weijia/djangoautoconf

.. image:: https://pypip.in/d/djangoautoconf/badge.png
        :target: https://crate.io/packages/djangoautoconf?version=latest


Create a package for ease setting django project settings.

* Free software: BSD license
* Documentation: http://djangoautoconf.rtfd.org.


Installation
------------

::

    python setup.py install
    
    
Create Project
----------------------------

::


    Create manage.py
    Added the following:
    
    #!/usr/bin/env python
    import logging
    import os
    import sys

    from ufs_tools import get_sibling_folder
    from ufs_tools.folder_tool import get_file_folder
    from ufs_tools.libtool import include_all_direct_sub_folders_in_sibling


    # include_all_direct_sub_folders_in_sibling(__file__, "server_base_packages")


    if __name__ == "__main__":
        # logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('chronograph.models').setLevel(level=logging.DEBUG)
        from djangoautoconf import DjangoAutoConf

        # Additional settings can be made
        # os.environ["EXTRA_SETTING_FOLDER"] = get_sibling_folder(__file__, "local/local_postgresql_settings")
        # os.environ["MANAGE_PY"] = "manage_with.py"
        DjangoAutoConf.set_settings_env()

        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)


Features
--------

::

    r = AdminRegister()
    r.register(UserDefinedModel)

Default behavior
--------------------------------
* When "/"  is not defined, redirect to all_login app if it is added to INSTALLED_APPS



TODO
--------

### 向我捐助
如果你觉得本项目对你有用，欢迎请作者一杯茶。

|捐赠weijia2000|

.. |捐赠weijia2000| image:: https://t.alipayobjects.com/images/mobilecodec/TB1ej3RXXmyMeJjm2EPXXaZrFXa

Work around for module installation.
        'django-ajax-selects<=1.9.1'
        'python-social-auth<=0.2.21'
