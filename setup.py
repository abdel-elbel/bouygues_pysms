from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import bouygues_pysms

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt', 'CHANGES.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='bouygues_pysms',
    version=bouygues_pysms.__version__,
    url='http://github.com/jeffknupp/bouygues_pysms/',
    license='Apache Software License',
    author='Jeff Knupp',
    tests_require=['pytest'],
    install_requires=['requests',
                    'Flask-SQLAlchemy>=1.0',
                    'SQLAlchemy==0.8.2',
                    ],
    cmdclass={'test': PyTest},
    author_email='jeff@jeffknupp.com',
    description='Automated REST APIs for existing database-driven systems',
    long_description=long_description,
    packages=['bouygues_pysms'],
    include_package_data=True,
    platforms='any',
    test_suite='tests.test_bouygues_pysms',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)