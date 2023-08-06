#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='stonedatalib3',
    version='0.2.4',
    description=(
        '<量化思想>'
    ),
    long_description=open('README.rst').read(),
    author='Q',
    author_email='stonedata@stonedata.co',
    maintainer='Q',
    maintainer_email='Q@stonedata.co',
    license='BSD License',
	package_dir={'': 'stonedatalib'},
    packages=[''],
	include_package_data=True,
	exclude_package_date={'':['MANIFEST.in','README.rst','setup.py']},
    platforms=["all"],
    url='https://www.stonedata.co//',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pandas',
        'numpy',
        'protobuf>=3.6.1',
		'grpcio'
    ]
)
