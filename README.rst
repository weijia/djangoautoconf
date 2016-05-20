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
    
    
Create Poject
------------

::


    Create "manage.py"
    Added the following:
    
    import logging
    import sys

    from ufs_tools.libtool import include_all

    if __name__ == "__main__":
        # logger.setLevel(logging.DEBUG)
        include_all(__file__, "server_base_packages")
        from djangoautoconf import DjangoAutoConf
        DjangoAutoConf.set_settings_env()

        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)


Features
--------

::

    r = AdminRegister()
    r.register(UserDefinedModel)

Default behavior
--------
* When "/"  is not defined, redirect to all_login app if it is added to INSTALLED_APPS



TODO
--------
