#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ckpt2tfserving',
    version='1.0.4',
    keywords=('tensorflow serving', 'checkpoint model'),
    description='a simple tool which can convert tensorflow checkpoint model file to tensorflow serving format.',
    license='MIT License',
    install_requires=['tensorflow>=1.1.0'],
    author='Andy Cheung',
    author_email='im@andy-cheung.me',
    packages=find_packages(),
    platforms='any',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ckpt_to_tfserving=tools.ckpt_to_tfserving:main'
        ]
    }
)
