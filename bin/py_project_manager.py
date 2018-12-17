#!/usr/bin/env python

import os
import sys
import argparse
import shutil
import subprocess

HOME_DIR = os.path.expanduser('~')


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


DEFAULT_FILES = [
    DefaultFile('setup.py'), DefaultFile('setup.cfg'), DefaultFile('README.md'),
    DefaultFile('MANIFEST.in'), DefaultFile('tox.ini', TOX_CONTENT),
    DefaultFile('.travis.yml', TRAVIS_CONTENT)
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
            # create subdir project __init__.py file
            self.create_file(os.path.join(fullpath, name, '__init__.py'))

        # create subdir
        for subdir in subdirs:
            self.create_dir(os.path.join(fullpath, subdir))

        # create files
        for default_file in DEFAULT_FILES:
            self.create_file(
                os.path.join(fullpath, default_file.name), default_file.content.format(name=name).strip())

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
    parser = argparse.ArgumentParser(prog='py_project_manager', description='Simple tool to create python project')

    subparsers = parser.add_subparsers(help='commands')
    startsproject_parser = subparsers.add_parser('startsproject')
    startsproject_parser.add_argument(
        'startsproject', action=StartsProjectAction, nargs=1, help='Path of the project directory')

    startsproject_parser.add_argument('--git', action='store_true', default=False, help='Initialize project as git project')
    startsproject_parser.add_argument('--venv', action='store_true', default=False, help='Initialize project and create the corresponding virtual env')
    startsproject_parser.add_argument('--reset', action='store_true', default=False, help='Reset an empty project')
    startsproject_parser.add_argument('--django', action='store_true', default=False, help='Starts a django project')

    args = parser.parse_args()
