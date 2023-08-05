#!/usr/bin/env python2
#-*-coding:utf-8-*-

from setuptools import setup, find_packages

# 获取package描述信息
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="wxlog",
    version="0.2",
    author="wangxing",
    author_email="wangxing1217@126.com",
    license="MIT License",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # add
    install_requires=[]
)
