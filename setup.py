#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import os.path
import warnings

requirements = [
    'Flask >= 0.10.1',
]

extras_require = {
    'doc': [
        'Sphinx',
    ],
    'test': [
        'pytest >2.5',
        'pytest-timeout',
        'mock',
    ],
}

dependency_links = [
]

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Framework :: Flask',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


def readme():
    try:
        root = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(root, 'README.rst')) as f:
            return f.read()
    except IOError:
        warnings.warn("Couldn't found README.rst", RuntimeWarning)
        return ''


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests/', 'flask_factory/']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='Flask-Factory',
    version='0.1.0dev',
    author='Eunchong Yu',
    author_email='kroisse@gmail.com',
    maintainer='Eunchong Yu',
    maintainer_email='kroisse@gmail.com',
    url='https://github.com/Kroisse/flask-factory',
    license='BSD',
    description='Provide a general-purpose application factory of the Flask '
                'application, and the configurator that is independent of the '
                'app object.',
    long_description=readme(),
    packages=find_packages(where='.'),
    include_package_data=True,
    zip_safe=True,
    install_requires=requirements,
    extras_require=extras_require,
    tests_require=extras_require['test'],
    cmdclass={
        'test': PyTest,
    },
    dependency_links=dependency_links,
    classifiers=classifiers,
)
