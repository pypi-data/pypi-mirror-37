#!/usr/bin/env python

from setuptools import setup, Extension

setup(
    # Application name:
    name="sshplaces",

    # Version number (initial):
    version=open("VERSION.txt").readline().rstrip(),

    # Application author details:
    author="Steven hk Wong",
    author_email="steven@wongsrus.net",

    # Packages
    packages=["sshplaces", "sshplaces/classes"],

    # Include additional files into the package
    include_package_data=True,

    package_data={'sshplaces': [ 'LICENSE.txt', 'README.txt', 'CHANGES.txt' , 'classes/README.txt', 'classes/servers.yaml']},

		scripts=[ 'scripts/sshplaces' ],

    # Details
    url="http://pypi.python.org/pypi/sshplaces/",

    #
    license="GNU GENERAL PUBLIC LICENSE",
    description="A curses menu of ssh places.",

    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=['yaml-utilities'],
)
