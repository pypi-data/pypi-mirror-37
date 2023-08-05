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
    'version': '0.1.1',
    'description': 'Python implementation of ciphersweet',
    'long_description': '# pyciphersweet\nPython implementation of ciphersweet\n\nThis is a very early stage implementation of ciphersweet from https://github.com/paragonie/ciphersweet\nPlease do not attempt to use this in production yet, as I\'m not sure if everything works. There are tests that match the original ciphersweet tests and those tests are currently passing.\n\nCurrently, only the "modern" modes are supported.\n\nHere is an example of how to create an encrypted field of the last four digits of a number:\n\n    import ciphersweet\n    import secrets\n    \n    nacl_key = secrets.token_bytes(32)\n    field = ciphersweet.EncryptedField(\n        base_key=nacl_key,\n        table=\'contacts\',\n        field=\'ssn\',\n    )\n    t = ciphersweet.Transformation.last_four_digits\n    field.add_blind_index(\'contact_ssn_last_four\', t, output_length=16, fast=True)\n    index = field.get_blind_index(\'hello\', name=\'contact_ssn_last_four\')\n    \n    print(index[\'value\'])\n    \nFor documentation on how this works, look into the original ciphersweet project.\n\n',
    'author': 'J. Ryan Littlefield',
    'author_email': 'ryan@ryanlittlefield.com',
    'url': 'https://github.com/rlittlefield/pyciphersweet',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
