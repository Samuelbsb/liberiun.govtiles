# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
    )

setup(name='liberiun.govtiles',
    version=version,
    description="Tiles para o Portal Padrao",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='liberiun portal padrao tiles cover governo federal',
    author='Liberiun',
    author_email='',
    url='http://www.github.com/liberiun/liberiun.govtiles',
    license='GPL version 2',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=['liberiun', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.cover',
        'sc.social.like',
        ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.testing',
            'mock',
            ],
        },
    entry_points="""
    # -*- entry_points -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
