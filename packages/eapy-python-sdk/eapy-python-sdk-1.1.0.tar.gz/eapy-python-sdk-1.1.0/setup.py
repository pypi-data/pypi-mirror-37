#!/usr/bin/env python
import setuptools
from distutils.core import setup

setup(name='eapy-python-sdk',
      version='1.1.0',
      description='Eapy python sdk',
      author='Marco Mendao',
      author_email='mac.mendao@gmail.com',
      url='http://marcomendao.betacode.tech',
      install_requires=[
            'requests',
      ],
      packages=[
            'eapy_python_sdk'
      ]
)
