#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zsql',
    version='1.0.2',
    py_modules=['zsql'],
    author='zlyuan',
    author_email='1277260932@qq.com',
    packages=find_packages(),
    description='简单的mysql封装库, 使用非常简单, 直接调用方法操作, 不需要再去想sql代码了',
    long_description=open('description.txt', 'r', encoding='utf8').read(),  # 项目介绍
    url='https://pypi.org/',
    license='GNU GENERAL PUBLIC LICENSE',
    platforms=['all'],
    scripts=['description.txt'],  # 额外的文件
    install_requires=['pymysql'],  # 依赖库
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
