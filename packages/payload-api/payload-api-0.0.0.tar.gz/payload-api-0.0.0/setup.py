import os
import sys
from io import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dist_name = 'payload-api'
pkg_name = 'payload'

install_requires = ['requests']

directory = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(directory, pkg_name))
from __about__ import __version__

with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=dist_name,
    version=__version__,
    description='Payload python library',
    author='Payload',
    author_email='help@payload.co',
    url='https://github.com/payload-code/payload-python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[pkg_name],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
