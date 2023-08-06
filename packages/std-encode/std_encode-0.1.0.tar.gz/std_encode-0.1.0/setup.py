# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['std_encode']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cram>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['std_encode = std_encode:console.run']}

setup_kwargs = {
    'name': 'std-encode',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jaime Buelta',
    'author_email': 'jaime.buelta@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
