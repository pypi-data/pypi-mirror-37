#!/usr/bin/env python3

import os

from setuptools import setup
from setuptools.command.install import install


class InstallScript(install):

    def run(self):
        install.run(self)
        # change file permission because pip keeps removing them
        os.chmod(os.path.dirname(os.path.abspath(__file__)) + '/ghnotifier/settings.py', 0o775)


setup(
    name='ghnotifier',
    version='0.1.4',
    description='Github notifications.',
    url='http://github.com/kunicmarko20/ghnotifier',
    author='Marko Kunic',
    author_email='kunicmarko20@gmail.com',
    license='MIT',
    packages=['ghnotifier'],
    scripts=['bin/ghnotifier'],
    install_requires=[
        'configparser',
        'requests'
    ],
    cmdclass={'install': InstallScript},
    zip_safe=False,
    include_package_data=True
)
