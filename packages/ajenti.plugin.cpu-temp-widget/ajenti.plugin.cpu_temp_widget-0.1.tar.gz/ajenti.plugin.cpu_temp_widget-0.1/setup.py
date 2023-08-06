#!/usr/bin/env python
from setuptools import setup, find_packages

import os

__requires = filter(None, open('requirements.txt').read().splitlines())

setup(
    name='ajenti.plugin.cpu_temp_widget',
    version='0.1',
    install_requires=__requires,
    description='CPU Temp widget',
    long_description='CPU Temp widget plugin for Ajenti panel',
    author='Yuriy Yurinskiy',
    author_email='yuriyyurinskiy@yandex.ru',
    url='https://yuriyyurinskiy.ru',
    packages=find_packages(),
    include_package_data=True,
)