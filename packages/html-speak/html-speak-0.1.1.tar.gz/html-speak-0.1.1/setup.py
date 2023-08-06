# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['html_speak']

package_data = \
{'': ['*']}

install_requires = \
['falcon>=1.4,<2.0',
 'gunicorn>=19.9,<20.0',
 'regex==2018.02.21',
 'ttslib>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'html-speak',
    'version': '0.1.1',
    'description': 'HTML TTS server for Chinese/Japanese and Jupyter Notebook',
    'long_description': "# html-speak\n\nHTML TTS server for Chinese/Japanese and Jupyter Notebook.\n\n## Usage\n\n```python\nfrom html_speak import SpeakServer\nserver = SpeakServer(lang='zh_cn')\nserver.view(JSON_SERIALIZABLE_OBJ)\n```\n\n## Screenshots\n\n![](/screenshots/0.png?raw=true)\n\n## Installation\n\n```commandline\npip install html-speak\n```\n\n## Related projects\n\n- [ttslib](https://github.com/patarapolw/ttslib) - \nTTS for both online and local usage that works\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/html-speak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
