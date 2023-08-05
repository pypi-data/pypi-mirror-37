#!/usr/bin/env python3

import tiv as project

from setuptools import setup, find_packages
import os

def here(*path):
    return os.path.join(os.path.dirname(__file__), *path)

def get_file_contents(filename):
    with open(here(filename), 'r', encoding='utf8') as fp:
        return fp.read()

setup(
    name = project.__name__,
    description = project.__doc__.strip(),
    long_description=get_file_contents('README.md'),
    url = 'https://gitlab.com/nul.one/' + project.__name__,
    download_url = 'https://gitlab.com/nul.one/{1}/-/archive/{0}/{1}-{0}.tar.gz'.format(project.__version__, project.__name__),
    version = project.__version__,
    author = project.__author__,
    author_email = project.__author_email__,
    license = project.__license__,
    packages = [ project.__name__ ],
    entry_points={ 
        'console_scripts': [
            '{0}={0}.__main__:cli'.format(project.__name__),
        ],
    },
    install_requires = [
        'Pillow>=3.1.2,<4.0',
        'cairosvg>=2.2.1,<2.3',
        'click>=6.7.0,<8.0',
        'numpy>=1.15.1,<2.0',
    ],
    python_requires=">=3.4.6",
)

