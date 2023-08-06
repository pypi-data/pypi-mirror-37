# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon',
 'dophon.annotation',
 'dophon.annotation.req',
 'dophon.annotation.res',
 'dophon.def_prop',
 'dophon.logger',
 'dophon.properties']

package_data = \
{'': ['*']}

install_requires = \
['Flask_Bootstrap',
 'PyMySQL',
 'dophon-manager',
 'flask',
 'gevent',
 'schedule',
 'urllib3']

setup_kwargs = {
    'name': 'dophon',
    'version': '1.2.9.post1',
    'description': 'dophon web framework like springboot',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
