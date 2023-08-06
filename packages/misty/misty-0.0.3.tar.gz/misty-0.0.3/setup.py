"""
Copyright (c) 2018 by Riptide I/O
All rights reserved.
"""

import os
import sys

from setuptools import setup
from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel

class BinaryDistWheel(bdist_wheel):
    def finalize_options(self):
	bdist_wheel.finalize_options(self)
	self.root_is_pure = False

# This creates a list which is empty but returns a length of 1.
# Should make the wheel a binary distribution and platlib compliant.
class EmptyListWithLength(list):
    def __len__(self):
        return 1


def setup_packages():

    long_description=""
    with open('README.txt') as f:
        long_description = f.read()

    meta_data = dict(
	name="misty",
	version='0.0.3',
	description='MSTP support for bacpypes',
	author='Riptide, Inc',
	author_email='info@riptideio.com',
	maintainer='Riptide, Inc',
	maintainer_email='raghavan@riptideio.com',
	url='https://bitbucket.org/riptideio/rtdds',
        zip_safe = False,
        cmdclass={'bdist_wheel': BinaryDistWheel},

        package_data = {
            # directory: [list of files that you want to pick up]
            'mstplib': ['libmstp_agent.so'],
            'examples':['*.ini', '*.history']
        },
        packages=['mstplib', 'examples'],
        ext_modules=EmptyListWithLength(),


	install_requires=[
	    "bacpypes"
	]
    )
    setup(**meta_data)
	


if __name__ == '__main__':
    setup_packages()
