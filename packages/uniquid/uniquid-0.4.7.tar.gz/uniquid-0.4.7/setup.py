# Copyright (c) 2018 UniquID

"""
Configuration file for setuptools and pip.
"""

import sys
import platform
from setuptools import setup, find_packages
from os import path
import uniquid.core.constants as constants

min_version = (str(constants.MIN_VERSION_MAJOR)
               + '.' + str(constants.MIN_VERSION_MINOR))

if (sys.version_info <
        (constants.MIN_VERSION_MAJOR, constants.MIN_VERSION_MINOR)):
    print('Current Python version: ' + platform.python_version())
    sys.exit('Incorrect version of Python installed. Python < ' +
             min_version + ' is not supported.')

current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'USER.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='uniquid',
    version=constants.APP_VERSION,
    description='Uniquid command line administration tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Uniquid Inc.',
    author_email='hello@uniquid.com',
    maintainer='Michael McCarthy',
    maintainer_email='mmccarthy@uniquid.com',
    url='http://uniquid.com/',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: System Administrators',
                 'License :: Other/Proprietary License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Security',
                 'Topic :: System :: Systems Administration'],
    packages=find_packages(),
    data_files=[('.', ['LICENSE', 'CHANGELOG.md', 'USER.md'])],
    include_package_data=True,
    python_requires='>=' + min_version,
    install_requires=[
        'click>=6.7',
        'requests>=2.19',
        'jsonschema>=2.6',
        'pycrypto>=2.6.1'
    ],
    entry_points='''
        [console_scripts]
        uniquid=uniquid.cli:cli_group
    ''',
)
