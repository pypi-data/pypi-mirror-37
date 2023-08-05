# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tinydb_viewer']

package_data = \
{'': ['*'], 'tinydb_viewer': ['templates/*']}

install_requires = \
['flask>=1.0,<2.0',
 'pyexcel-text>=0.2.7,<0.3.0',
 'pyexcel>=0.5.9,<0.6.0',
 'python-dateutil>=2.7,<3.0',
 'requests>=2.19,<3.0',
 'tinydb>=3.11,<4.0']

setup_kwargs = {
    'name': 'tinydb-viewer',
    'version': '0.2.7',
    'description': 'View records generated from TinyDB and alike (e.g. list of dictionaries.)',
    'long_description': "# tinydb-viewer\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/tinydb-viewer.svg)](https://pypi.python.org/pypi/tinydb-viewer/)\n[![PyPI license](https://img.shields.io/pypi/l/tinydb-viewer.svg)](https://pypi.python.org/pypi/tinydb-viewer/)\n\nView records generated from [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) and alike (e.g. list of dictionaries.)\n\n## Installation\n\nMethod 1:\n\n```commandline\n$ pip install tinydb-viewer\n```\n\nMethod 2:\n\n- Clone the project from GitHub\n- [Get poetry](https://github.com/sdispater/poetry) and `poetry install tinydb-viewer --path PATH/TO/TINYDB/VIEWER`\n\n## Usage\n\nRun a server initiation script first. This will allow you to edit the data as well.\n\n```python\nfrom tinydb_viewer import TinyDB\nTinyDB('db.json').runserver()\n```\n\nThen, in IPython or in Jupyter Notebook,\n\n```python\n>>> from tinydb_viewer import TinyDB\n>>> tdb = TinyDB('db.json')\n>>> tdb.search(tdb.query['foo'] == 'bar', sort_func=lambda x: x['baz'])\n>>> tdb.view()\n'The first page is shown.'\n>>> tdb.view(-1)\n'The last page is shown.'\n>>> tdb.previous()\n'The previous page (i-1) is shown.'\n>>> tdb.next()\n'The next page (i+1) is shown.'\n```\n\n## Bonus\n\nI extended TinyDB a little. My TinyDB is `'ensure_ascii' = False` by default, so that the file is a little smaller.\n\nAlso, it will use [tinydb-constraint](https://github.com/patarapolw/tinydb-constraint) by default, if it is installed.\n\n## Screenshots\n\n![](/screenshots/jupyter0.png?raw=true)\n\n## Related projects\n\n- [tinydb-constraint](https://github.com/patarapolw/tinydb-constraint) - Apply constraints before inserting and updating TinyDB records.\n",
    'author': 'Pacharapol Withyasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/tinydb-viewer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
