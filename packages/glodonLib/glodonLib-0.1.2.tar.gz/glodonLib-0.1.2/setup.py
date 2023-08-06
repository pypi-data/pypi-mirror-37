# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: uppengfei
#############################################


from setuptools import setup, find_packages

setup(
    name="glodonLib",
    version="0.1.2",
    keywords=("pip", "glodonLib"),
    description="common functions",
    long_description="common functions",
    license="MIT Licence",

    url="https://github.com/upengfei/glodonLib",
    author="upengfei",
    author_email="yu.pf@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="win32",
    install_requires=[
        'requests',
        'redis',
        'xlrd',
    ]
)
