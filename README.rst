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

    django-admin createproject example
    
    Create extra_settings folder
    
    Create extra_settings/settings.py
    
    Remove lines in manage.py
    Added the following:
    
    from djangoautoconf import DjangoAutoConf
    #Added keys folder to path so DjangoAutoConf can find keys in it
    c = DjangoAutoConf()
    c.set_default_settings("example.settings")
    #Added root folder to path so DjangoAutoConf can find django root
    c.set_root_dir(get_folder(__file__))
    c.add_extra_settings(["extra_settings.settings"])
    #c.configure(['mysql_database', ])


Features
--------

* TODO