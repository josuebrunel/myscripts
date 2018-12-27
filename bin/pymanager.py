#!/usr/bin/env python

import datetime
import os
import sys
import argparse
import shutil
import subprocess

HOME_DIR = os.path.expanduser('~')


LICENSE_CONTENT = """
MIT License

Copyright (c) {date.year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files ({name}), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


MANIFEST_CONTENT = """
include requirements.txt
include README.rst
include version.py
"""


SETUPCFG_CONTENT = """
[metadata]
description-file = README.md
"""


SETUP_CONTENT = """
import os
from setuptools import setup, find_packages
import subprocess

__author__ = '{author}'
__email__ = '{email}'
name = '{name}'

version_py = os.path.join(os.path.dirname(__file__), 'version.py')

try:
    version_git = subprocess.check_output(["git", "describe"]).rstrip()
except Exception:
    with open(version_py, 'r') as fh:
        version_git = open(version_py).read().strip().split('=')[-1].replace('"', '')

version_msg = "# Do not edit this file, pipeline versioning is governed by git tags"

with open(version_py, 'w') as fh:
    fh.write(version_msg + os.linesep + "__version__=" + version_git)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


url = "https://github.com/%s/%s/" % (__author__, name)
download_url = url + 'archive/{version}.tar.gz'.format(version=version_git)
requirements = read('requirements.txt').splitlines()

setup(
    name=name,
    version=version_git,
    description="{description}",
    long_description=read("README.rst"),
    author=__author__,
    author_email=__email__,
    url=url,
    download_url=download_url,
    keywords=[],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
    platforms=['Any'],
    license='MIT',
    install_requires=requirements
)
"""


TOX_CONTENT = """
[tox]
envlist = py27, py35

[testenv]
deps=
    pytest
    coverage
commands=
    - python -m coverage run --source={name} -m pytest -vvs tests/
    - python -m coverage report -m
"""

TRAVIS_CONTENT = """
sudo: false
language: python
python:
    - '2.7'
    - '3.5'
install:
    - pip install coverage coveralls
script:
    - python -m coverage run --source={name} -m pytest -vs tests/
after_success:
    - python -m coverage report
    - coveralls
"""


def run_bash_command(command, cwd='.'):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=cwd, shell=True)
    result = process.communicate()
    return result


class DefaultFile(object):

    def __init__(self, name, content=''):
        self.name = name
        self.content = content

    def __str__(self):
        return self.content.strip()

    def __repr__(self):
        return '<DefaultFile: %s>' % self.name


DEFAULT_FILES = [
    DefaultFile('setup.py', SETUP_CONTENT), DefaultFile('setup.cfg', SETUPCFG_CONTENT),
    DefaultFile('README.rst'), DefaultFile('MANIFEST.in', MANIFEST_CONTENT),
    DefaultFile('tox.ini', TOX_CONTENT), DefaultFile('.travis.yml', TRAVIS_CONTENT),
    DefaultFile('LICENSE', LICENSE_CONTENT)
]


class StartsProjectAction(argparse.Action):

    def __call__(self, parser, namespace, value, options=None):
        fullpath = value[0]
        basepath, name = os.path.split(fullpath)
        subdirs = [name, 'tests']

        if namespace.django:
            command = 'django-admin startproject %s' % name
            run_bash_command(command)
            subdirs.pop(subdirs.index(name))
        else:
            self.create_dir(fullpath, namespace.reset)

        # create subdir
        for subdir in subdirs:
            self.create_dir(os.path.join(fullpath, subdir))

        # create subdir project __init__.py file
        self.create_file(os.path.join(fullpath, name, '__init__.py'))

        # create files
        context = {
            'name': name.capitalize(), 'author': '{author}', 'email': '{email}',
            'description': '', 'version': '{version}',
            'date': datetime.datetime.now()
        }
        for default_file in DEFAULT_FILES:
            self.create_file(
                os.path.join(fullpath, default_file.name), default_file.content.format(**context).strip())

        # initialize as git project
        if namespace.git:
            self.git_init(fullpath)

        # create virtualenv
        if namespace.venv:
            self.mkvirtualenv(name)

    def create_dir(self, dirname, reset=False):
        if reset:
            shutil.rmtree(dirname)
        try:
            os.mkdir(dirname)
        except (OSError,) as e:
            print('Error: %s' % e.strerror)
            sys.exit(1)
        return True

    def create_file(self, filename, content=''):
        with open(filename, 'wb') as fd:
            fd.write(content)

    def git_init(self, project_dir):
        commands = [
            'git init',
            'git add -A',
            'git commit -m "starts project"'
        ]

        for cmd in commands:
            run_bash_command(cmd, cwd=project_dir)

    def mkvirtualenv(self, name):
        try:
            import virtualenv
        except (ImportError,) as e:
            print('Error: %s' % e.strerror)
            sys.exit(1)
        virtualenv.create_environment(os.path.join(HOME_DIR, '.virtualenvs', name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='pymanager', description='Simple tool to create python project')

    subparsers = parser.add_subparsers(help='commands')
    startsproject_parser = subparsers.add_parser('start')
    startsproject_parser.add_argument(
        'start', action=StartsProjectAction, nargs=1, help='Start a project')

    startsproject_parser.add_argument('--git', action='store_true', default=False, help='Initialize project as git project')
    startsproject_parser.add_argument('--venv', action='store_true', default=False, help='Initialize project and create the corresponding virtual env')
    startsproject_parser.add_argument('--reset', action='store_true', default=False, help='Reset an empty project')
    startsproject_parser.add_argument('--django', action='store_true', default=False, help='Starts a django project')

    args = parser.parse_args()
