# -*- coding:utf-8 -*-

import os
from setuptools import setup


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'flaskcap', 'version.py')) as f:
        variables = {}
        exec(f.read(), variables)

        version = variables.get('VERSION')
        if version:
            return version

    raise RuntimeError('No version info found.')


setup(
    name='flaskcap',
    version=get_version(),
    author='Vincent',
    description='Flask-based web framework, including orm with connection pool',
    long_description=open('README.rst').read(),
    license='APACHE',
    packages=['flaskcap'],
    platforms='Unix',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,',
    install_requires=[
        'flask>=0.7',
        'orator>=0.9',
        'DBUtils>=1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
