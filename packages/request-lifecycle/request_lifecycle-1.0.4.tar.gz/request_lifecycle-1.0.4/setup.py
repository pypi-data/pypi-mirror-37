# Copyright 2018 Frank Lin. All Rights Reserved.
# -*- coding: utf-8 -*-

import setuptools
import io
import re

with open('README.md', 'r') as fh:
    readme = fh.read()

with io.open('request_lifecycle/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setuptools.setup(
    name='request_lifecycle',
    version=version,
    author='Frank Lin',
    author_email='lin.xiaoe.f@gmail.com',
    description='Request lifecycle logger for flask',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='http://git.azure.gagogroup.cn/efficiency/request-lifecyle-logger-python',
    packages=['request_lifecycle'],
    python_requires='>3.6.0',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Framework :: Flask',
    ],
    install_requires=[
        'Flask>=0.12.2',
        'requests>=2.18.4'
    ]
)
