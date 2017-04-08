#!/usr/bin/env python

import os
import argparse

DEFAULT_FILES = ['setup.py', 'README.md', 'MANIFEST.in']


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

    def create_dir(self, dirname):
        os.mkdir(dirname)
        return True

    def create_file(self, filename, content=''):
        with open(filename, 'wb') as fd:
            fd.write(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='py_project_manager', description='Simple tool to create python project')

    subparsers = parser.add_subparsers(help='commands')
    startsproject_parser = subparsers.add_parser('startsproject')
    startsproject_parser.add_argument(
        'startsproject', action=StartsProjectAction, nargs=1, help='Path of the project directory')

    args = parser.parse_args()
