#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zforeach',
    version='1.0.0',
    py_modules=['zforeach'],
    author='zlyuan',
    author_email='1277260932@qq.com',
    packages=find_packages(),
    description='对基本类型dict, list, set, tuple进行遍历, 并对遍历的数据进行操作',
    # long_description=open('README.md','r',encoding='utf8').read(),  # 项目介绍
    url='https://pypi.org/',
    license='GNU GENERAL PUBLIC LICENSE',
    platforms=['all'],
    scripts=[],  # 额外的文件
    install_requires=[],  # 依赖库
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
