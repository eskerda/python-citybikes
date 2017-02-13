# -*- coding: utf-8 -*-

import re

from setuptools import setup, find_packages

with open('citybikes/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.rst', 'r') as f:
    readme = f.read()
with open('HISTORY.rst', 'r') as f:
    history = f.read()

setup(
    name='python-citybikes',
    version=version,
    description='Client interface for the Citybikes API',
    long_description=readme + '\n\n' + history,
    author='Lluís Esquerda',
    author_email='eskerda@gmail.com',
    url='http://github.com/eskerda/python-citybikes',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'requests',
        'six',
    ],
    tests_require=[
        'pytest',
        'responses',
    ],
    keywords='Citybikes api.citybik.es bike sharing',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
