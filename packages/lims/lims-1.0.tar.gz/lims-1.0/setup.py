#!/usr/bin/env python
# -*- coding=utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='lims',
    version='1.0',
    author='suqingdong',
    author_email='suqingdong@novogene.com',
    description='toolkits for lims',
    long_description=open('README.rst').read(),
    url='https://github.com/suqingdong/lims',
    license='BSD License',
    install_requires=['requests>=2.10'],
    packages=find_packages(),
    include_package_data=True,
    scripts=['lims/bin/lims.py'],
    # entry_points={'console_scripts': [
    #     'lims = lims.bin.main',
    # ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],

)
