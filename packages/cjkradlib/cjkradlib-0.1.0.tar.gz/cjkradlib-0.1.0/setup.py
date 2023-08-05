# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cjkradlib', 'cjkradlib.data', 'cjkradlib.data.jp', 'cjkradlib.data.zh']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>=1.0,<2.0']

setup_kwargs = {
    'name': 'cjkradlib',
    'version': '0.1.0',
    'description': 'Generate compositions, supercompositions and variants for a given Hanzi / Kanji',
    'long_description': "# CJKradlib\n\nGenerate compositions, supercompositions and variants for a given Hanzi / Kanji.\n\n## Installation\n\n```commandline\npip install cjkradlib\n```\n\n## Usage\n\n```python\nfrom cjkradlib import RadicalFinder\nfinder = RadicalFinder(lang='zh')  # default is 'zh'\nresult = finder.search('麻')\nprint(result.compositions)  # ['广', '林']\nprint(result.supercompositions)  # ['摩', '魔', '磨', '嘛', '麽', '靡', '糜', '麾']\nprint(result.variants)  # ['菻']\n```\n\nSupercompositions are based on the character frequency in each language, so altering the language give slightly different results.\n\n```python\nfrom cjkradlib import RadicalFinder\nfinder = RadicalFinder(lang='jp')\nresult = finder.search('麻')\nprint(result.supercompositions)  # ['摩', '磨', '魔', '麿']\n```\n\n## Related projects\n\n- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp)\n- [ChineseViewer](https://github.com/patarapolw/ChineseViewer)\n- [CJKrelate](https://github.com/patarapolw/CJKrelate)\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/cjkradlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
