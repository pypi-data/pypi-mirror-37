# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['str2port']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['str2port = str2port.__main__:cli']}

setup_kwargs = {
    'name': 'str2port',
    'version': '0.1.1',
    'description': 'Convert string to md5 hash, then to port number. No randomization involved.',
    'long_description': "# str2port\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/str2port.svg)](https://pypi.python.org/pypi/str2port/)\n[![PyPI license](https://img.shields.io/pypi/l/str2port.svg)](https://pypi.python.org/pypi/str2port/)\n\nConvert string to md5 hash, then to port numbers. No randomization involved.\n\nEvery time you run the script, it will return the same port numbers.\n\n## Installation\n\n```commandline\npip install str2port\n```\n\n## Usage\n\n`str2port` is available is a CLI app,\n\n```commandline\n$ str2port --help\nUsage: str2port [OPTIONS] STRING\n\nOptions:\n  --use-iana  Exclude used ports from IANA list (default: false)\n  --help      Show this message and exit.\n$ str2port imserv\n29635 44619 3226 6562 52589 12473 1423 1026\n$ str2port imserv\n29635 44619 3226 6562 52589 12473 1423 1026\n```\n\nOf course, it is also accessible via a Python script\n\n```python\n>>> from str2port import str2port\n>>> str2port('imserv')\n[29635, 44619, 3226, 6562, 52589, 12473, 1423, 1026]\n```\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/str2port',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
