#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'ipython',
    'future',
]

setup(
    name='ipyfuturize',
    version='0.0.1',
    description="%%futurize magic for ipython",
    long_description=readme,
    author="Douglas La Rocca",
    author_email='doug@larocca.io',
    url='https://github.com/douglas-larocca/ipyfuturize',
    packages=[
        'ipyfuturize',
    ],
    package_dir={'ipyfuturize':
                 'ipyfuturize'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='futurize 2to3 ipython magic',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)