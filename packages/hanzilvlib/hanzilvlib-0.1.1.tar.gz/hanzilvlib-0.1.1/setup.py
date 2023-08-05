# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hanzilvlib', 'hanzilvlib.data']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'cjkradlib>=0.1.1,<0.2.0',
 'importlib_resources>=1.0,<2.0',
 'jieba>=0.39.0,<0.40.0',
 'requests>=2.19,<3.0',
 'wordfreq>=2.2,<3.0']

setup_kwargs = {
    'name': 'hanzilvlib',
    'version': '0.1.1',
    'description': 'A library to view contents from HanziLevelProject, plus some popular dictionaries.',
    'long_description': '# HanziLvLib\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)\n[![PyPI license](https://img.shields.io/pypi/l/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)\n\nA library to view contents from [HanziLevelProject](http://hanzilevelproject.blogspot.com/#!), plus some popular dictionaries.\n\n## Features\n\n- Hanzi meanings, variants, components and supercompositions, sorted by Hanzi frequency.\n- Built-in CE-DICT and sorted by vocab frequency.\n- Sentences from [Chinese Sentences and audio, spoon fed](https://ankiweb.net/shared/info/867291675), and if inadequate, from [Jukuu](http://jukuu.com)\n\n## Installation\n\n```commandline\npip install hanzilvlib\n```\n\n## Usage\n\nThe contents are contained in two subpackages:-\n\n- `hanzilvlib.dictionary`\n- `hanzilvlib.level`\n\nPlease see [/example.ipynb](https://github.com/patarapolw/hanzilvlib/blob/master/example.ipynb).\n\n## Related projects\n\n- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp) - A Hanzi learning suite, with levels based on Hanzi Level Project, aka. another attempt to clone WaniKani.com for Chinese.\n- [CJKradlib](https://github.com/patarapolw/cjkradlib) - Generate compositions, supercompositions and variants for a given Hanzi / Kanji\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/hanzilvlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
