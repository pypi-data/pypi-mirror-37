# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pype']

package_data = \
{'': ['*']}

install_requires = \
['attrs',
 'bump2version>=0.5.10,<0.6.0',
 'click',
 'click-default-group',
 'parso',
 'toolz',
 'twisted']

entry_points = \
{'console_scripts': ['pype = pype:app.cli']}

setup_kwargs = {
    'name': 'python-pype',
    'version': '0.0.53',
    'description': '',
    'long_description': 'pype: command-line pipes in Python\n####################################\n\nUsage\n=====\n\n\n\n\nAt the command prompt, use ``pype`` to act on each item in the file with python commands: ::\n\n  $ printf \'abc\' | pype str.upper\n\n  ABC\n\n\nChain python functions together with ``!``: ::\n\n  $ printf \'Hello\'  | pype \'str.upper ! len\'\n\n  5\n\nUse ``?`` as a placeholder for the input at each stage: ::\n\n  $ printf \'Hello World\'  | pype \'str.split ! ?[0].upper() + "!"\'\n\n  HELLO!\n\n  $ printf \'Hello World\'  | pype \'str.split ! ?[0].upper() + "!" ! ?.replace("H", "J")\'\n\n  JELLO!\n\n\n\nGiven a server responding to ``http://localhost:8080/`` and a list of urls in ``urls.txt`` : ::\n\n  http://localhost:8080/Requester_254\n  http://localhost:8080/Requester_083\n  http://localhost:8080/Requester_128\n  http://localhost:8080/Requester_064\n  http://localhost:8080/Requester_276\n\n\nAutomatically import required modules and use their functions: ::\n\n   $ pype \'str.strip ! requests.get ! ?.text \' < urls.txt\n\n   Hello, Requester_254. You are client number 7903 for this server.\n   Hello, Requester_083. You are client number 7904 for this server.\n   Hello, Requester_128. You are client number 7905 for this server.\n   Hello, Requester_064. You are client number 7906 for this server.\n   Hello, Requester_276. You are client number 7907 for this server.\n\n\nUse ``map`` to act on each input item (``map`` is the default command). Use ``apply`` to act on the sequence of items. Finding the largest number returned from the server: ::\n\n    $ pype --newlines=no map \'str.strip ! requests.get ! ?.text ! ?.split()[6] ! int\' apply \'max\'  < urls.txt\n\n    7933\n\n\nMaking sequential requests is slow. Use ``--async`` to make I/O really fast (see caveats below). ::\n\n  $ time pype \'str.strip ! requests.get ! ?.text\'  < urls.txt\n\n  Hello, Requester_254. You are client number 8061 for this server.\n  Hello, Requester_083. You are client number 8062 for this server.\n  Hello, Requester_128. You are client number 8063 for this server.\n  Hello, Requester_064. You are client number 8064 for this server.\n  Hello, Requester_276. You are client number 8065 for this server.\n\n  real\t0m10.640s\n  user\t0m0.548s\n  sys\t0m0.022s\n\n\nMaking concurrent requests is much faster: ::\n\n   $ time pype --async \'str.strip ! treq.get ! treq.text_content\'  < urls.txt\n\n   Hello, Requester_254. You are client number 8025 for this server.\n   Hello, Requester_083. You are client number 8025 for this server.\n   Hello, Requester_128. You are client number 8025 for this server.\n   Hello, Requester_064. You are client number 8025 for this server.\n   Hello, Requester_276. You are client number 8025 for this server.\n\n   real\t0m2.626s\n   user\t0m0.574s\n   sys\t0m0.044s\n\n\n\nInstallation\n============\n\n``pip install python-pype``\n\n\nCaveats\n=======\n\n\n* ``pype`` assumes *trusted command arguments* and *untrusted input stream data*. It uses ``eval`` on your arguments, not on the input stream data. If you use ``exec``, ``eval``, ``subprocess``, or similar commands, you can execute arbitrary code from the input stream.\n\n* ``--async`` currently works only with ``map``, not ``apply`` and works only for a single ``map`` pipe-string, e.g. ``map \'str.upper ! len ! ? & 1\'``, not for chains, e.g. ``map str.upper map len map \'? & 1\'``.\n\n\n\n\nStatus\n======\n\n* Check the `issues page <https://www.github.com/python-pype/pype/issues>`_ for open tickets.\n* This package is experimental pre-alpha and is subject to change.\n\n\nRelated work\n============\n\n* https://github.com/Russell91/pythonpy\n* http://gfxmonk.net/dist/doc/piep/\n* https://spy.readthedocs.io/en/latest/intro.html\n* https://github.com/ksamuel/Pyped\n* https://github.com/ircflagship2/pype\n',
    'author': 'author',
    'author_email': 'author@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
