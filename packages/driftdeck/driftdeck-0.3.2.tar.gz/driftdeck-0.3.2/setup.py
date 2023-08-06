# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['driftdeck']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6,<0.7', 'markdown>=3,<4']

entry_points = \
{'console_scripts': ['driftdeck = driftdeck.core:start']}

setup_kwargs = {
    'name': 'driftdeck',
    'version': '0.3.2',
    'description': 'Drift Deck eats markdown files and spits out beautiful slides directly into your browser.',
    'long_description': '# driftdeck\n\nDrift Deck eats markdown files and spits out beautiful slides directly into your browser.\n\n## How do you use it?\n\n```\n$ driftdeck myslides.md\n```\n\nYour web browser should open a a new tab at `http://localhost:{SOMEPORT}/1` and display your slides.\n\n## Where can you get it?\n\n### [PyPI][pypi]\n\n```\npip install driftdeck\n```\n\n### [Archlinux AUR][aur]\n\n```\npacaur -S python-driftdeck\n```\n\n### [Gitlab][gitlab]\n\n```\ngit clone https://gitlab.com/XenGi/driftdeck\n```\n\n## How can you improve it?\n\nYou need poetry which you can install with pipsi:\n\n```\npipsi install poetry\n```\n\nThen clone the repo, install the dependencies and run it:\n\n```\ngit clone https://gitlab.com/XenGi/driftdeck\ncd driftdeck\npoetry install\npoetry run driftdeck\n```\n\n\n[pypi]: https://pypi.org/project/driftdeck/\n[aur]: https://aur.archlinux.org/packages/python-driftdeck/\n[gitlab]: https://gitlab.com/XenGi/driftdeck\n',
    'author': 'Ricardo Band',
    'author_email': 'email@ricardo.band',
    'url': 'https://gitlab.com/XenGi/driftdeck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
