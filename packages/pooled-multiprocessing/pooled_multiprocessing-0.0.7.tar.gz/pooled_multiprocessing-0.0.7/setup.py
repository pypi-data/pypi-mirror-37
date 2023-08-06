#!/user/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except Exception:
    readme = ''


setup(
    name="pooled_multiprocessing",
    version="0.0.7",
    url='https://github.com/namuyan/pooled_multiprocessing',
    author='namuyan',
    description='Simple pooled multiprocessing',
    long_description=readme,
    packages=find_packages(),
    install_requires=['psutil', 'more_itertools'],
    license="MIT Licence",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
