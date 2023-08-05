#!/usr/bin/env python3

from setuptools import setup, find_packages
import tiv

setup(
    name = 'tiv',
    description = tiv.__doc__.strip(),
    url = 'https://github.com/nul-one/tiv',
    download_url = 'https://github.com/nul-one/tiv/archive/'+tiv.__version__+'.tar.gz',
    version = tiv.__version__,
    author = tiv.__author__,
    author_email = tiv.__author_email__,
    license = tiv.__licence__,
    packages = [ 'tiv' ],
    entry_points={ 
        'console_scripts': [
            'tiv=tiv.__main__:main',
        ],
    },
    install_requires = [
        'Pillow>=3.1.2,<4.0',
        'numpy>=1.15.1,<2.0',
        'click>=6.7.0,<8.0',
    ],
    python_requires=">=3.4.6",
)

