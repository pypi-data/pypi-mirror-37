"""
Copyright (c) 2018 by Riptide I/O
All rights reserved.
"""

import os
import sys

from setuptools import setup

long_description = '''
misty

The misty project helps build bacpypes Applications that work on MS/TP Networks.
The BIP (BACnet IP ) Applications can be easily ported to use misty.
'''

def setup_packages():

    meta_data = dict(
	name="misty",
	version='0.0.2',
	description='MSTP support for bacpypes',
        long_description=long_description,
	author='Riptide, Inc',
	author_email='raghavan@riptideio.com',
	maintainer='Riptide, Inc',
	maintainer_email='raghavan@riptideio.com',
        url='https://github.com/riptideio/misty',
        zip_safe = False,
        license='Apache2',

        package_data = {
            'mstplib': ['libmstp_agent.so'],
        },
        packages=['mstplib'],

	install_requires=[
	    "bacpypes"
	]
    )
    setup(**meta_data)
	


if __name__ == '__main__':
    setup_packages()
