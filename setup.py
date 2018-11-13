from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import bouygues_pysms

here = os.path.abspath(os.path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    long_description = open('README.md').read()
    
setup(
    name='bouygues_pysms',
    version=bouygues_pysms.__version__,
    url='https://github.com/abdel-elbel/bouygues_pysms/',
    license=io.open('LICENSE', encoding='utf-8').read().encode("utf-8"),
    author='Abdel El Bel',
    install_requires=['requests',
                     're'
                     ],
    author_email='abdel.elbel@gmail.com',
    description='This module is a Python interface to Bouygues Mobile SMS API',
    long_description=long_description,
    packages=['bouygues_pysms'],
    include_package_data=True,
    platforms='any',
    test_suite='tests.test_bouygues_pysms',
    classifiers = [
        'Programming Language :: Python',
#        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],

)