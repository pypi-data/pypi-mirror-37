# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['berny']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0']

entry_points = \
{'console_scripts': ['berny = berny.cli:main']}

setup_kwargs = {
    'name': 'pyberny',
    'version': '0.3.5',
    'description': 'Molecular/crystal structure optimizer',
    'long_description': "# `berny` — Molecular optimizer\n\n[![build](https://img.shields.io/travis/azag0/pyberny/master.svg)](https://travis-ci.org/azag0/pyberny)\n[![coverage](https://img.shields.io/codecov/c/github/azag0/pyberny.svg)](https://codecov.io/gh/azag0/pyberny)\n![python](https://img.shields.io/pypi/pyversions/pyberny.svg)\n[![pypi](https://img.shields.io/pypi/v/pyberny.svg)](https://pypi.org/project/pyberny/)\n[![commits since](https://img.shields.io/github/commits-since/azag0/pyberny/latest.svg)](https://github.com/azag0/pyberny/releases)\n[![last commit](https://img.shields.io/github/last-commit/azag0/pyberny.svg)](https://github.com/azag0/pyberny/commits/master)\n[![license](https://img.shields.io/github/license/azag0/pyberny.svg)](https://github.com/azag0/pyberny/blob/master/LICENSE)\n\nThis Python 2/3 package can optimize molecular and crystal structures with respect to total energy, using nuclear gradient information.\n\nIn each step, it takes energy and Cartesian gradients as an input, and returns a new structure estimate.\n\nThe algorithm is an amalgam of several techniques, comprising redundant internal coordinates, iterative Hessian estimate, trust region, line search, and coordinate weighing, mostly inspired by the optimizer in the [Gaussian](http://gaussian.com) program.\n\n## Installing\n\nInstall and update using [Pip](https://pip.pypa.io/en/stable/quickstart/):\n\n```\npip install -U pyberny\n```\n\n## Example\n\n```python\nfrom berny import Berny, geomlib\n\noptimizer = Berny(geomlib.readfile('geom.xyz'))\nfor geom in optimizer:\n    # get energy and gradients for geom\n    optimizer.send((energy, gradients))\n```\n\n## Links\n\n- Documentation: <https://azag0.github.io/pyberny>\n",
    'author': 'Jan Hermann',
    'author_email': 'dev@janhermann.cz',
    'url': 'https://github.com/azag0/pyberny',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
