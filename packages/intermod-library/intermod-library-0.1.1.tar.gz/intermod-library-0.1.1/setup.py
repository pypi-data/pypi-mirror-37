# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['intermod_library']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'pandas>=0.23,<0.24',
 'scipy>=1.1,<2.0']

setup_kwargs = {
    'name': 'intermod-library',
    'version': '0.1.1',
    'description': 'A library of tools for finding and viewing intermodulation products and harmonics',
    'long_description': '=========================\nIntermod Libray\n=========================\n\nTools for finding and viewing intermodulation products and harmonics\n====================================================================\n\nSource can be found at:\nhttps://github.com/wboxx1/intermod-library\n\nDocumentation can be found at:\nhttps://wboxx1.github.io/intermod-library/docs/build/html/index.html\n\nInstallation:\n--------------\n\nUsing pip::\n\n    pip install intermod-library\n\n',
    'author': 'Will Boxx',
    'author_email': 'wboxx1@gmail.com',
    'url': 'https://wboxx1.github.io/intermod-library/build/html/index.html',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
