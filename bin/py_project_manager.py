#!/usr/bin/env python

import os
import sys
import argparse
import subprocess


DEFAULT_FILES = ['setup.py', 'setup.cfg', 'README.md', 'MANIFEST.in']


def run_bash_command(command, cwd='.'):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=cwd, shell=True)
    result = process.communicate()
    return result


class StartsProjectAction(argparse.Action):

    def __call__(self, parser, namespace, value, options=None):
        fullpath = value[0]
        basepath, name = os.path.split(fullpath)

        self.create_dir(fullpath)

        # create subdir
        for subdir in (name, 'tests'):
            self.create_dir(os.path.join(fullpath, subdir))

        # create subdir project __init__.py file
        self.create_file(os.path.join(fullpath, name, '__init__.py'))

        # create files
        for default_file in DEFAULT_FILES:
            self.create_file(os.path.join(fullpath, default_file))

        # initialize as git project
        if namespace.git:
            self.git_init(fullpath)

    def create_dir(self, dirname):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py_project_manager', description='Simple tool to create python project')

    subparsers = parser.add_subparsers(help='commands')
    startsproject_parser = subparsers.add_parser('startsproject')
    startsproject_parser.add_argument(
        'startsproject', action=StartsProjectAction, nargs=1, help='Path of the project directory')

    startsproject_parser.add_argument('--git', action='store_true', default=False, help='Initialize project as git project')

    args = parser.parse_args()
