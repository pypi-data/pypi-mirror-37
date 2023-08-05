# -*- coding: utf-8 -*-
"""Installer for the cciaapd.contenttypes package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='cciaapd.contenttypes',
    version='1.2.0',
    description="Content types for cciaapd",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='https://github.com/PloneGov-IT/cciaapd.contenttypes',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['cciaapd'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'z3c.jbot',
        'plone.app.dexterity',
        'plone.directives.dexterity',
        'plone.app.contenttypes',
        'plone.app.versioningbehavior',
        'plone.app.lockingbehavior',
	    'plone.app.referenceablebehavior',
        'rer.bandi',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes[atrefs]<1.2',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
