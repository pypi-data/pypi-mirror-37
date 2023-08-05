#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from authlib.consts import version, homepage


def fread(filename):
    with open(filename) as f:
        return f.read()


client_requires = ['requests']
crypto_requires = ['cryptography']


setup(
    name='Authlib',
    version=version,
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    url=homepage,
    packages=find_packages(include=('authlib', 'authlib.*')),
    description=(
        'The ultimate Python library in building OAuth and '
        'OpenID Connect servers.'
    ),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    long_description=fread('README.rst'),
    license='GNU AGPLv3+',
    install_requires=client_requires + crypto_requires,
    project_urls={
        'Bug Tracker': 'https://github.com/lepture/authlib/issues',
        'Documentation': 'https://docs.authib.org/',
        'Source Code': 'https://github.com/lepture/authlib',
        'Blog': 'https://blog.authlib.org/',
        'Sponsor': 'https://www.patreon.com/lepture',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
