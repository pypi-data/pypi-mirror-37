# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cjkradlib',
 'cjkradlib.data',
 'cjkradlib.data.cjkvi_ids',
 'cjkradlib.data.jp',
 'cjkradlib.data.zh']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>=1.0,<2.0']

setup_kwargs = {
    'name': 'cjkradlib',
    'version': '0.1.2',
    'description': 'Generate compositions, supercompositions and variants for a given Hanzi / Kanji',
    'long_description': "# CJKradlib\n\n[![Build Status](https://travis-ci.org/patarapolw/cjkradlib.svg?branch=master)](https://travis-ci.org/patarapolw/cjkradlib)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/cjkradlib.svg)](https://pypi.python.org/pypi/cjkradlib/)\n[![PyPI license](https://img.shields.io/pypi/l/cjkradlib.svg)](https://pypi.python.org/pypi/cjkradlib/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/cjkradlib.svg)](https://pypi.python.org/pypi/cjkradlib/)\n\nGenerate compositions, supercompositions and variants for a given Hanzi / Kanji, based on [cjkvi-ids](https://github.com/cjkvi/cjkvi-ids). (Previously, [cjk-decomp](https://github.com/amake/cjk-decomp).)\n\n## Installation\n\n```commandline\npip install cjkradlib\n```\n\nAlso, IDS sequences use full range of CJK ideographs, so the fonts\nthat covers all encoded ideographs (such\nas [HanaMin](http://fonts.jp/hanazono/)\nor [Hanamin AFDKO](https://github.com/cjkvi/HanaMinAFDKO/releases) )\nshould be used.\n\n## Usage\n\n```python\nfrom cjkradlib import RadicalFinder\nfinder = RadicalFinder(lang='zh')  # default is 'zh'\nresult = finder.search('麻')\nprint(result.compositions)  # ['广', '林']\nprint(result.supercompositions)  # ['摩', '魔', '磨', '嘛', '麽', '靡', '糜', '麾']\nprint(result.variants)  # ['菻']\n```\n\nSupercompositions are based on the character frequency in each language, so altering the language give slightly different results.\n\n```python\nfrom cjkradlib import RadicalFinder\nfinder = RadicalFinder(lang='jp')\nresult = finder.search('麻')\nprint(result.supercompositions)  # ['摩', '磨', '魔', '麿']\n```\n\n## Related projects\n\n- [ChineseViewer](https://github.com/patarapolw/ChineseViewer)\n- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp)\n- [CJKrelate](https://github.com/patarapolw/CJKrelate)\n\n## Plan\n\n- Use https://github.com/cjkvi/cjkvi-ids as the source for CJK-decomposition.\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/cjkradlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
