#!/usr/bin/env python3

from setuptools import setup

setup(
    name='ghnotifier',
    version='0.1.3',
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
    zip_safe=False,
    include_package_data=True
)
