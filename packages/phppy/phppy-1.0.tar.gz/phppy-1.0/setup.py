#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='phppy',
    version='1.0',
    description=(
        'let you can use like php language to use python,include some function and PDO (base on pymysql)'
    ),
    long_description=open('README.rst').read(),
    author='dreammo',
    author_email='dreammovip@163.com',
    maintainer='dreammo',
    maintainer_email='dreammovip@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/dream-mo/pyphp',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pymysql>=0.9.2'
    ]
)

