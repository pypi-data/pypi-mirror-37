#!/usr/bin/python3
# coding:utf-8
 
import os
import sys
#from distutils.core import setup
from setuptools import setup
from setuptools import Command, find_packages 
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
from shutil import rmtree

# meta-data
NAME = 'autoargparse'
DESCRIPTION = 'Make CMD arg-parser easy and simple.'
URL = 'https://github.com/gLhookniano/autoargparse'
EMAIL = 'gLhookniano@protonmail.com'
AUTHOR = 'gLhookniano'
VERSION = '0.1.0'
LICENCE = 'MIT'
REQUIRED = ['']


here = os.path.abspath(os.path.dirname(__file__))
# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('>>>{0}'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree('./dist')
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')
        
        self.status('Publishing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')
        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=LICENCE,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=[''],# Required
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.

    python_requires='>=3.5.0',
    py_modules=['autoargparse'],

    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    cmdclass={
        'upload': UploadCommand,
    },
    
    zip_safe=False
    )
