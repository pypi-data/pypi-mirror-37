# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hypdb',
 'hypdb.core',
 'hypdb.modules.infotheo',
 'hypdb.modules.kbutil',
 'hypdb.modules.kbutil.build.lib.kbutil',
 'hypdb.modules.pyrankagg',
 'hypdb.modules.pyrankagg.build.lib.pyrankagg',
 'hypdb.modules.pyrankagg.build.lib.pyrankagg.tests',
 'hypdb.modules.pyrankagg.kbutil',
 'hypdb.modules.pyrankagg.tests',
 'hypdb.modules.site-packages',
 'hypdb.modules.statistics']

package_data = \
{'': ['*'], 'hypdb': ['modules/lpsolve_dev/*', 'utils/*']}

install_requires = \
['matplotlib',
 'numba>=0.39.0,<0.40.0',
 'numpy-indexed>=0.3.5,<0.4.0',
 'pandas>=0.23.4,<0.24.0',
 'psycopg2>=2.7.5,<3.0.0',
 'rpy2>=2.9.4,<3.0.0',
 'scipy>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'hypdb',
    'version': '0.0.7',
    'description': 'HypDB: Detect, Explain And Resolve Bias in OLAP (think twice about your group-by query)',
    'long_description': '# HypDB\nThe core HypDB module lives in the `HypDB/` directory. A web UI demo that demonstrates the capabilities of HypDB lives in the `demo/` directory.\n\n### PyPI\nOur package is published on PyPI [here](https://pypi.org/project/hypdb/).\n\n### Paper\nOur paper (published in VLDB 2018 in Rio de Janeiro) can be found [here](https://drive.google.com/file/d/1YJ-Up3imD2UhdoyYyfXBPng5iy70jtrh/view?usp=sharing).\n\n### Contributing\nWe follow [angular-style commit message guidelines.](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)\n\nTo write code to solve an issue, branch off from master and name the branch with something unique and descriptive. We may open a PR at any stage of solving an issue, but request for code review when it might be ready to merge back into master. We can close the respective issue once the PR has been merged.\n',
    'author': 'Corey Cole',
    'author_email': 'coreylc@uw.edu',
    'url': 'http://db.cs.washington.edu/projects/hypdb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
