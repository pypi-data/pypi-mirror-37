# -*- coding: utf-8 -*-
#
#   mete0r.recipe.whoami : a zc.buildout recipe to know whoami
#   Copyright (C) 2014-2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import with_statement
from contextlib import contextmanager
import os.path
import re
import sys


def setup_dir(f):
    ''' Decorate f to run inside the directory where setup.py resides.
    '''
    setup_dir = os.path.dirname(os.path.abspath(__file__))

    def wrapped(*args, **kwargs):
        with chdir(setup_dir):
            return f(*args, **kwargs)

    return wrapped


@contextmanager
def chdir(new_dir):
    old_dir = os.path.abspath(os.curdir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


@setup_dir
def import_setuptools():
    try:
        import setuptools
        return setuptools
    except ImportError:
        pass

    import ez_setup
    ez_setup.use_setuptools()
    import setuptools
    return setuptools


@setup_dir
def readfile(path):
    if sys.version_info.major == 3:
        f = open(path, encoding='utf-8')
    else:
        f = open(path)
    with f:
        return f.read()


@setup_dir
def get_version():
    source = readfile('src/mete0r/recipe/whoami/__init__.py')
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              source, re.M)
    if not version_match:
        raise RuntimeError('Unable to find version string.')
    return version_match.group(1)


def alltests():
    import sys
    import unittest
    import zope.testrunner.find
    import zope.testrunner.options
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    args = sys.argv[:]
    defaults = ['--test-path', here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)


install_requires_filename = 'requirements.in'
install_requires = readfile(install_requires_filename)

tests_require = readfile('requirements/test.in')


setup_info = {
    'name': 'mete0r.recipe.whoami',
    'version': get_version(),
    'description': 'a zc.buildout recipe to know whoami',
    'long_description': readfile('README.rst') + readfile('CHANGES.rst'),

    'author': 'mete0r',
    'author_email': 'mete0r@sarangbang.or.kr',
    'license': 'GNU Lesser General Public License v3 or later (LGPLv3+)',
    'url': 'https://github.com/mete0r/recipe.whoami',

    'namespace_packages': [
        'mete0r',
        'mete0r.recipe',
    ],
    'packages': [
        'mete0r',
        'mete0r.recipe',
        'mete0r.recipe.whoami'
    ],
    'package_dir': {
        '': 'src'
    },
    'install_requires': install_requires,
    'test_suite': '__main__.alltests',
    'tests_require': tests_require,
    'extras_require': {
        'test': tests_require,
    },
    'entry_points': {
        'zc.buildout': [
            'default = mete0r.recipe.whoami:Recipe'
        ],
    },
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Buildout :: Recipe',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    'keywords': [
        'zc.buildout', 'recipe', 'whoami'
    ],
    'zip_safe': True,
}


@setup_dir
def main():
    setuptools = import_setuptools()
    setuptools.setup(**setup_info)


if __name__ == '__main__':
    main()
