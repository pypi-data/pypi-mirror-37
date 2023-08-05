# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyvid']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner>=0.1.8,<0.2.0',
 'click>=7.0,<8.0',
 'ffmpeg-python>=0.1.16,<0.2.0',
 'hurry.filesize>=0.9.0,<0.10.0',
 'pytoml>=0.1.19,<0.2.0']

entry_points = \
{'console_scripts': ['pyvid = pyvid:main']}

setup_kwargs = {
    'name': 'pyvid',
    'version': '0.0.7',
    'description': 'Video conversion utility using ffmpeg',
    'long_description': '# pyvid 0.0.6-alpha\n\n[![PyPI version](https://badge.fury.io/py/pyvid.svg)](https://badge.fury.io/py/pyvid)\n[![Build Status](https://travis-ci.org/0jdxt/pyvid.svg?branch=master)](https://travis-ci.org/0jdxt/pyvid)\n[![Documentation Status](https://readthedocs.org/projects/pyvid/badge/?version=latest)](https://pyvid.readthedocs.io/en/latest/?badge=latest)\n[![Coverage Status](https://coveralls.io/repos/github/0jdxt/pyvid/badge.svg?branch=master)](https://coveralls.io/github/0jdxt/pyvid?branch=master)\n\n## Dependencies\n\n- [install](https://www.ffmpeg.org/download.html)\n  ffmpeg and make sure the executable is in PATH\n\n## Installation\n\nInstall as global executable\n\n```\npip install pyvid\n```\n\n## Usage\n\nThe following\n\n```\npyvid files -e avi\n```\n\nwill convert all `.avi` files in directory `files/` to output directory `converted/files/`\n\nUses defaults on ffmpeg executable to get high quality and low file size.\n\n```\nUsage: pyvid [OPTIONS] FOLDER\n\nOptions:\n  -e, --ext TEXT  File extension to look for\n  -y, --force     Disable convert prompt\n  -d, --rem       Delete source video file(s)\n  --version       Show the version and exit.\n  --help          Show this message and exit.\n```\n',
    'author': 'jdxt',
    'author_email': 'jytrn@protonmail.com',
    'url': 'https://github.com/0jdxt/pyvid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
