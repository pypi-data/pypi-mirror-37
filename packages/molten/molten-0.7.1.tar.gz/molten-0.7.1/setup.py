# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['molten',
 'molten.http',
 'molten.openapi',
 'molten.openapi.templates',
 'molten.testing',
 'molten.validation']

package_data = \
{'': ['*'], 'molten': ['contrib/*']}

install_requires = \
['typing-extensions>=3.6,<4.0', 'typing-inspect>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'molten',
    'version': '0.7.1',
    'description': 'A minimal, extensible, fast and productive API framework.',
    'long_description': '# molten\n\n[![Build Status](https://travis-ci.org/Bogdanp/molten.svg?branch=master)](https://travis-ci.org/Bogdanp/molten)\n[![PyPI version](https://badge.fury.io/py/molten.svg)](https://badge.fury.io/py/molten)\n[![Documentation](https://img.shields.io/badge/doc-latest-brightgreen.svg)](https://moltenframework.com)\n[![Reddit](https://img.shields.io/badge/discuss-online-orange.svg)](https://www.reddit.com/r/moltenframework/)\n\n*A minimal, extensible, fast and productive API framework for Python 3.*\n\n<hr/>\n\n**Changelog**: https://moltenframework.com/changelog.html <br/>\n**Community**: https://www.reddit.com/r/moltenframework/ <br/>\n**Documentation**: https://moltenframework.com\n\n<hr/>\n\n\n## Installation\n\n    pip install molten\n\n\n## Quickstart\n\nCheck out the [examples] folder to get a taste of the framework or\nread the [user guide]!\n\n\n## License\n\nmolten is licensed under the LGPL.  Please see [COPYING] and\n[COPYING.LESSER] for licensing details.\n\n[COPYING.LESSER]: https://github.com/Bogdanp/molten/blob/master/COPYING.LESSER\n[COPYING]: https://github.com/Bogdanp/molten/blob/master/COPYING\n[examples]: https://github.com/Bogdanp/molten/blob/master/examples\n[user guide]: https://moltenframework.com/guide.html\n',
    'author': 'Bogdan Popa',
    'author_email': 'bogdan@cleartype.io',
    'url': 'https://moltenframework.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
