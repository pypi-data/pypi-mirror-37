# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

VERSION = "1.0.0.dev2"
AUTHOR = "Agência Municipal de Tecnologia da Informação do Município de Palmas"
AUTHOR_EMAIL = 'dev.licencas@palmas.to.gov.br'

LONG_DESCRIPTION = """
Boilerplate Manager is a Django app to generate forms, templates, API,
views for apps of your project. For each app in your project, you create
the models and after you can generate all the forms, templates, APIs and
views of this app, you will only need to take care of the business rule.

Github: https://github.com/agencia-tecnologia-palmas/boilerplate-manager/blob/master/README.md

"""
# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='boilerplate-manager',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='It is a Django app to generate forms, templates, Api Rest and views for apps of your project.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/agencia-tecnologia-palmas/boilerplate-manager.git',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "django>=2.1",
        "django-cors-headers>=2.4.0",
        "djangorestframework>=3.8.2",
        "requests>=2.19.1"
    ]
)