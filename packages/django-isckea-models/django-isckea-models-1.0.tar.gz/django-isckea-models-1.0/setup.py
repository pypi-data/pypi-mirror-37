#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='django-isckea-models',
    version='1.0',
    url='https://bitbucket.org/code-orange/django-isckea-models/',
    download_url='https://bitbucket.org/code-orange/django-isckea-models/downloads/',
    license='LGPL version 3 or later',
    description='ISC Kea models for Django',
    long_description=open('README.rst').read(),
    author='Kevin Olbrich',
    author_email='ko@sv01.de',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.2',
    ],
)
