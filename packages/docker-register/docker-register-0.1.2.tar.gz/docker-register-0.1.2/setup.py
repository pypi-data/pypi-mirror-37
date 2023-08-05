#!/usr/bin/env python

from distutils.core import setup

setup(
    # Application name:
    name="docker-register",

    # Version number (initial):
    version=open("VERSION.txt").readline().rstrip(),

    # Application author details:
    author="Steven hk Wong",
    author_email="steven@wongsrus.net",

    # Packages
    packages=["docker-register", "docker-register/classes"  ],

    # Include additional files into the package
    include_package_data=True,

    package_data={'docker-register': [ 'classes/ssl/*', 'classes/templates/*', 'LICENSE.txt', 'README.txt', 'CHANGES.txt' , 'HISTORY.txt', 'classes/README.txt', ]},

		scripts=[ 'scripts/docker-register' ],

    # Details
    url="http://pypi.python.org/pypi/docker-register/",

    #
    license="LICENSE.txt",
    description="A in-memory register for Docker services and containers with published ports and labels.",

    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    requires=["docker", "jsonpickle", "flask" ],
)
