#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: RH
# Mail: sculizhenghao@foxmail.com
# Created Time:  2018-10-14 18:04:28
#############################################


from setuptools import setup, find_packages

setup(
    name = "RHTool",
    version = "0.1.0",
    keywords = ("pip", "RHTool","rhtool"),
    description = "RH packet",
    long_description = "This is a tool from RH， if you have any problem, please contat sculizhenghao@foxmail.com",
    license = "MIT Licence",

    url = "https://github.com/fengmm521/pipProject",
    author = "mage",
    author_email = "mage@woodcol.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
