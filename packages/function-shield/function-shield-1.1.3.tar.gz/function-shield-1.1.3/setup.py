#!/usr/bin/env python3
from setuptools import setup
from subprocess import Popen, PIPE
from os import path
from io import open

git_describe = ["git", "describe", "--abbrev=0", "--tags"]
version = Popen(git_describe, stdout=PIPE).communicate()[0].decode('utf-8')
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='function-shield',
    zip_safe=True,
    version=version,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PureSec',
    author_email='support@puresec.io',
    packages=['function_shield'],
    include_package_data=True
)
