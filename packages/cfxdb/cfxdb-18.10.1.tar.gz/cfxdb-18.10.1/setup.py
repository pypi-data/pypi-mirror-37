##############################################################################
#
#                        Crossbar.io Fabric
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from __future__ import absolute_import

from setuptools import setup, find_packages

# read package description
with open('README.rst') as f:
    long_description = f.read()

# read package version
with open('../crossbarfx/_version.py') as f:
    exec(f.read())  # defines __version__

setup(
    name='cfxdb',
    version=__version__,
    description='CrossbarFX edge ZLMDB database schema classes',
    long_description=long_description,
    author='Crossbar.io Technologies GmbH',
    author_email='support@crossbario.com',
    url='https://crossbario.com',
    license='proprietary',
    classifiers=['License :: Other/Proprietary License'],
    platforms=('Any'),
    install_requires=[
        'zlmdb>=18.10.1'
    ],
    packages=find_packages(),
    zip_safe=True
)
