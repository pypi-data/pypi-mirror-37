# -*- coding:utf-8 -*-

import setuptools


setuptools.setup(
    name="django-easy-jsonfield",
    version="0.0.1",
    author="claydodo and his little friends (xiao huo ban)",
    author_email="claydodo@foxmail.com",
    description="A fork of rpkilby's jsonfield2 (https://github.com/rpkilby/jsonfield2/), Aims to provide an easy django JSONField",
    url="https://github.com/claydodo/easy_jsonfield",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7 ",
        "Programming Language :: Python :: 3 ",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'six',
    ]
)
