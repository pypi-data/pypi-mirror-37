# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pypare', 'pypare.pypi', 'pypare.scripts']

package_data = \
{'': ['*'], 'pypare.pypi': ['templates/*']}

install_requires = \
['aiofile>=1.4,<2.0',
 'aiofiles>=0.4.0,<0.5.0',
 'aiohttp-jinja2>=1.1,<2.0',
 'aiohttp>=3.4,<4.0',
 'aiotask_context>=0.6.0,<0.7.0',
 'click>=7.0,<8.0',
 'colorama>=0.3.9,<0.4.0',
 'inotipy>=0.1.1,<0.2.0',
 'packaging>=18.0,<19.0',
 'structlog>=18.2,<19.0']

entry_points = \
{'console_scripts': ['pypare = pypare.scripts:main']}

setup_kwargs = {
    'name': 'pypare',
    'version': '0.3.3',
    'description': 'A very simple pypi cache',
    'long_description': 'pypare\n======\n\nA very simple pypi cache.\n\nfeatures\n^^^^^^^^\n\n- uses `aiohttp`_, `aiofiles`_, `inotipy`_\n\n- queries metadata via pypi JSON API\n\n- filesystem is the database\n\n- serve releases while downloading\n\n\n.. _`aiohttp`: http://aiohttp.readthedocs.io/\n.. _`aiofiles`: https://pypi.org/project/aiofiles/\n.. _`inotipy`: https://github.com/ldo/inotipy\n\ntodo\n^^^^\n\n- private channels with user, groups and permissions\n\n- use `python-libaio`_ for file stuff\n\n- nice ui\n\n.. _`python-libaio`: https://github.com/vpelletier/python-libaio\n\n\nrunning the cache\n^^^^^^^^^^^^^^^^^\n\n.. code-block::\n\n    # pypare --help\n    Usage: pypare [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n      --log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]\n                                      The logging level.  [default: INFO]\n      --loop [asyncio|uvloop]         Use a different loop policy.  [default:\n                                      asyncio]\n      --version                       Show the version and exit.\n      --help                          Show this message and exit.\n\n    Commands:\n      pypi  Run a simple pypi caching proxy.\n\n\n.. code-block::\n\n\n    # pypare pypi --help\n    Usage: pypare pypi [OPTIONS]\n\n      Run a simple pypi caching proxy.\n\n    Options:\n      -p, --port INTEGER              The port to run the server  [default: 3141]\n      -h, --host TEXT                 The server host IP.  [default: 0.0.0.0]\n      -b, --base-path PATH            The base path for this application.\n                                      [default: /pypi]\n      -c, --cache-root DIRECTORY      The cache directory, where files are stored.\n                                      [default: ~/.cache/pypare]\n      -u, --upstream-channel TEXT     The name of the upstream channel.\n      --upstream-channel-url TEXT     The base API URL of the upstream channel.\n      --upstream-channel-timeout INTEGER\n                                      The timeout upstream is asked for new\n                                      metadata.\n      --plugin LIST                   A plugin in pkg_resources notation to load.\n      --help                          Show this message and exit.\n\n\nRun from virtual environment:\n\n.. code-block:: bash\n\n   pip install pypare\n\n   pypare pypi --cache-root /tmp/pypi-data\n\n\nRun in docker:\n\n.. code-block:: bash\n\n   docker run -it diefans/pypare:latest pypi\n\n\nRun as zipapp:\n\n.. code-block:: bash\n\n   shiv pypare -c pypare -o ~/.local/bin/pypare -p ~/.pyenv/versions/3.7.0/bin/python\n\n   pypare pypi --cache-root /tmp/pypi-data\n\n\nUsing the cache\n^^^^^^^^^^^^^^^\n\n.. code-block:: bash\n\n   PIP_INDEX_URL=http://localhost:3141/pypi/pypi pip install tensorflow\n',
    'author': 'Oliver Berger',
    'author_email': 'oliver@digitalarchitekt.de',
    'url': 'https://github.com/diefans/pypare',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
