#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='djangoautoconf',
    version='0.2.0',
    description='Create a package for ease setting django project settings.',
    long_description=readme + '\n\n' + history,
    author='Richard Wang',
    author_email='richardwangwang@gmail.com',
    url='https://github.com/weijia/djangoautoconf',
    packages=[
        'djangoautoconf',
        'djangoautoconf.features',
        'djangoautoconf.ajax_select_utils',
        'djangoautoconf.class_based_views',
        'djangoautoconf.auto_conf_admin_tools',
        'djangoautoconf.django_rest_framework_utils',
        'djangoautoconf.settings_templates',
    ],
    package_dir={'djangoautoconf': 'djangoautoconf'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangoautoconf',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)