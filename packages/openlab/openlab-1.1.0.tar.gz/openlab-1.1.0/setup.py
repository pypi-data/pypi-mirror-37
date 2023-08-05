import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data
# Pull version from source without importing
# since we can't import something we haven't built yet :)
#exec(open('version.py').read())

NAME = "openlab"

REQUIRED = [
	"oauthlib", "requests", "requests-oauthlib", "validators", "datetime", "matplotlib", "uuid","numpy"
]

here = os.path.abspath(os.path.dirname(__file__))

setup(
	name = NAME,
	version='1.1.0',
	url='https://openlab.iris.no',
    #version=__version__,
	description = "A python client for OpenLab Drilling.",
	author='IRIS',
	author_email='andrew.holsaeter@norceresearch.no',
	license='IRIS COPYRIGHT: Do not distribute without approval by IRIS',
	packages = find_packages(),
	#packages=['openlab'],
	install_requires = REQUIRED,
	include_package_data = True,
	classifiers = [
		  # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.6',
		'Intended Audience :: Developers',
	]
)
