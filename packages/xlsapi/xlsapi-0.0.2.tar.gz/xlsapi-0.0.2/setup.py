#!/usr/bin/env python3
from setuptools import setup

version = '0.0.2'

setup(
    name = 'xlsapi',
    packages = ['xlsapi'],
    install_requires=[
        "Flask",
    ],
    version=version,
    description = 'serve XLS files as REST api',
    author = 'Thomas Irgang',
    author_email = 'thomas@irgang-la.de',
    url = 'https://gitlab.com/irgangla/xlsapi',
    download_url = 'https://gitlab.com/irgangla/xlsapi/archive/v' + version + '.tar.gz',
    keywords = ['XLS', 'Excel', 'REST', 'API'],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        ],
    long_description = """\
XLSAPI
-------------------------------------
Make "Excel databases" accessible as REST API.
"""
)
