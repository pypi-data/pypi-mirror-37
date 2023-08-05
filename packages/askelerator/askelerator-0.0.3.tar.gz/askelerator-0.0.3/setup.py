import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from distutils import dir_util
from pathlib import Path

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        __import__('pdb').set_trace()
        print("\n\n\n\nPOST INSTALL FOR DEV MODE\n\n\n")
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        print("\n\n\n\nPOST INSTALL FOR INSTALL MODE\n\n\n")
        install.run(self)

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


USER_DIR = str(Path.home()) + '/.askelerator'

if not os.path.isdir(USER_DIR):
    os.makedirs(USER_DIR)

dir_util.copy_tree('templates', USER_DIR + '/templates')

setup(
    name='askelerator',
    version='0.0.3',
    author='lfx',
    author_email='fx@zrkf.pw',
    description='A code skeleton generator for accelerated coding.',
    long_description=LONG_DESCRIPTION,
    #long_description_format='text/markdown',
    url='https://askelerator.pw',
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    #scripts=[
    #    'bin/askelerator'
    #],
    entry_points={
        'console_scripts': [
            'askelerator=askelerator.cli:main',
        ],
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    packages=['askelerator'],
)
