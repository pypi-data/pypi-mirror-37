# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['ciphersweet']
install_requires = \
['cryptography>=2.3,<3.0', 'pysodium>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'ciphersweet',
    'version': '0.1.0',
    'description': 'Python implementation of ciphersweet',
    'long_description': None,
    'author': 'J. Ryan Littlefield',
    'author_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
