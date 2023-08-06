#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

setup(
    name='fulfil_shop_flipgive',
    version='0.1.8',
    description="Flip Give Extension for Flip Give.",
    long_description=readme,
    author="Fulfil.io",
    author_email='info@fulfil.io',
    url='https://github.com/fulfilio/fulfil_shop_flipgive',
    packages=[
        'fulfil_shop_flipgive',
    ],
    package_dir={'fulfil_shop_flipgive':
                 'fulfil_shop_flipgive'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='fulfil_shop_flipgive',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
