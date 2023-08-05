# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['woo_sy']

package_data = \
{'': ['*']}

install_requires = \
['etsy_py>=1.0,<2.0',
 'python-wordpress-xmlrpc>=2.3,<3.0',
 'woocommerce>=1.2,<2.0']

setup_kwargs = {
    'name': 'woo-sy',
    'version': '0.1.0',
    'description': 'WooCommerce + Etsy = woo_sy | A tool for syncing listings between the two',
    'long_description': None,
    'author': 'Alexander VanTol',
    'author_email': 'alexander.m.vantol@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
