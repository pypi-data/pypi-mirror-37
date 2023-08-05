#!/usr/bin/env python
# coding: utf-8

'''_
# app_conf install


## Usage

    [sudo] ./setup.py install

----
'''

import os, sys
from setuptools import setup, find_packages


here = os.path.dirname(__file__)
with open(os.path.join(here, 'README.md')) as fd:
    md = fd.read()

with open(os.path.join(here, 'app_conf/version.py')) as fd:
    version = fd.read().split('=', 1)[1].split('\n', 1)[0]

# images hack for pypi:
# gh = 'https://raw.githubusercontent.com/axiros/terminal_markdown_viewer/master'
# md = md.replace('src="./', 'src="%s/' % gh)

PY2 = sys.version_info[0] < 3
inst_req = ['attrs', 'structlog', 'appdirs', 'colorama']
if PY2:
    inst_req.append('funcsigs')


setup(
    name='app_conf',
    version=version,
    packages=find_packages(),
    author='Axiros GmbH',
    author_email='gk@axiros.com',
    description='Application Config',
    install_requires=inst_req,
    extras_require={},
    long_description=md,
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='http://github.com/axiros/app_conf',
    download_url='http://github.com/axiros/app_conf/tarball/',
    keywords=['app', 'config', 'source code'],
    test_suite='nose.collector',
    tests_require=['nose', 'unittest2', 'coveralls'],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Code Generators',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={'console_scripts': ['appconf = app_conf:run']},
)
