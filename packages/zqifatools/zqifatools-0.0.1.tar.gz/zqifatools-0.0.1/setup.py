#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
    name='zqifatools',
    version='0.0.1',
    description='tools',
    long_description=open('README.rst').read(),
    author='Aaron Chu',
    author_email='zqifa@outlook.com',
    maintainer='aaron',
    maintainer_email='zqifa@outlook.com',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/zqifa',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
