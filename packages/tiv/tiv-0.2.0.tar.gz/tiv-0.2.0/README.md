Terminal Image Viewer
==================================================
[![Build Status](https://travis-ci.org/nul-one/tiv.png)](https://travis-ci.org/nul-one/tiv)
[![PyPI version](https://badge.fury.io/py/tiv.svg)](https://badge.fury.io/py/tiv)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Requirements Status](https://requires.io/github/nul-one/tiv/requirements.svg?branch=master)](https://requires.io/github/nul-one/tiv/requirements/?branch=master)

Print images (jpg, png, gif) in terminal.

Installation
-------------------------

### install from pypi (recommend)
`pip3 install tiv`

### install from git (latest master)
`pip3 install -U git+https://gitlab.com/nul.one/tiv.git`

Usage
-------------------------

`tiv [OPTIONS] IMAGE [IMAGE [IMAGE...]]`

### Options

- `-w, --width INTEGER` - Set image width in number of terminal characters. Default is 69.
- `-a, --aspect-ratio FLOAT` - Specify character aspect ratio (width:hight). Default is 0.5.


