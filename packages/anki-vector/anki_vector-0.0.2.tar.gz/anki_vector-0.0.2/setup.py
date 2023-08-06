# Copyright (c) 2018 Anki, Inc.

"""
Vector SDK, by Anki.

Requirements:
    * Python 3.6.1 or later
"""

import sys
from setuptools import setup

if sys.version_info < (3, 6, 1):
    sys.exit('The Anki Vector SDK requires Python 3.6.1 or later')

setup(
    name='anki_vector',
    version='0.0.2',
    description="SDK for Anki's Vector robot",
    long_description=__doc__,
    url='https://developer.anki.com',
    author='Anki, Inc',
    author_email='developer@anki.com',
    license='Apache License, Version 2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
    keywords='anki vector robot robotics sdk'.split(),
    packages=['anki_vector'],
)
