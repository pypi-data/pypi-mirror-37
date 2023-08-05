#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 2018/10/16

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='tmpserver',
        version='0.0.1',
        packages=['tmpserver'],
        url='https://github.com/xyok/tmpserver.git',
        license='MIT',
        author='xyok',
        author_email='xy___ok@163.com',
        description='create temporary http server quickily,and show qrcode in terminal',
        keywords=['http', 'server', "qrcode"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=[
            'qrcode'
        ],
        entry_points={
            'console_scripts': [
                'tmpserver = tmpserver.tmpserver:main'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)
