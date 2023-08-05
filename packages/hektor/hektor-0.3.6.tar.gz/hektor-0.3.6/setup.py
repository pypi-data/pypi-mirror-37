# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='hektor',
    version='0.3.6',
    description='A QTI-XML/XLS to JSON converter for humans',
    author='Jan Maximilian Michal',
    author_email='mail@janmax.org',
    url='https://gitlab.gwdg.de/j.michal/hektor',
    license='MIT',
    scripts=['bin/hektor'],
    install_requires=["lxml~=4.1.1",
                      "xlrd~=1.1.0",
                      "xkcdpass~=1.16.0"],
    py_modules=['hektor'],
    packages=['lib']
)
