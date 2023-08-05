# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hanzilvlib', 'hanzilvlib.data']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>=1.0,<2.0']

setup_kwargs = {
    'name': 'hanzilvlib',
    'version': '0.1.0',
    'description': 'A library to view contents from HanziLevelProject, plus some popular dictionaries.',
    'long_description': '# HanziLvLib\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)\n[![PyPI license](https://img.shields.io/pypi/l/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)\n\nA library to view contents from [HanziLevelProject](http://hanzilevelproject.blogspot.com/#!), plus some popular dictionaries.\n\n## Installation\n\n```commandline\npip install hanzilvlib\n```\n\n## Usage\n\nThe contents are contained in two subpackages:-\n\n### `hanzilvlib.dictionary`\n\n### `hanzilvlib.level`\n\n## Related projects\n\n- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp) - A Hanzi learning suite, with levels based on Hanzi Level Project, aka. another attempt to clone WaniKani.com for Chinese.\n- [CJKradlib](https://github.com/patarapolw/cjkradlib) - Generate compositions, supercompositions and variants for a given Hanzi / Kanji\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/hanzilvlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
