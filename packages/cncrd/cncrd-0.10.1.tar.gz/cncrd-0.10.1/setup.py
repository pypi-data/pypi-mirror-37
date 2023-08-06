# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['concord', 'concord.ext.base', 'concord.ext.base.filters']

package_data = \
{'': ['*']}

install_requires = \
['discord.py']

setup_kwargs = {
    'name': 'cncrd',
    'version': '0.10.1',
    'description': 'Middleware-based event processing library for Discord',
    'long_description': "# Concord\n\nMiddleware-based event processing library for Discord. Uses\n[discord.py](https://github.com/Rapptz/discord.py) under the hood.\n\n[![Build Status](https://img.shields.io/travis/narimanized/concord/dev.svg?style=flat-square)](https://travis-ci.org/narimanized/concord)\n[![Codecov](https://img.shields.io/codecov/c/github/narimanized/concord/dev.svg?style=flat-square)](https://codecov.io/gh/narimanized/concord)\n\nConcord **is not** a library for accessing Discord API. If you're here for an\nAPI library, see [discord.py](https://github.com/Rapptz/discord.py) or\n[disco](https://github.com/b1naryth1ef/disco), or\n[Discord Developer Documentation](https://discordapp.com/developers/docs/topics/community-resources)\npage with a list of libraries for different languages.\n\n## Purpose\n\nThe library aims to provide a more convenience way to handle Discord gateway\nevents, with code reusing where it's possible, including separating\nfunctionality into extensions.  \nEvent processing is done using the programmer-defined handlers tree. Like in web\napplications, due to similarity of the concepts of processing requests, Concord\ncalls these handlers as middleware as well.\n\nConcord doesn't try to be either a *fast* or a *slow* library. For it's\ncustomization ability, it had to pay the speed.\n\n## Example\n\n[Hugo](https://github.com/narimanized/hugo) - example bot, built on the Concord.\nTake a note, that there's no so much code. It just registers extensions -\nthird-party middleware sets.  \nActually, Concord - is a successor of Hugo. You can figure this out by the code\nhistory.\n\nExample extensions:\n[concord-ext-audio](https://github.com/narimanized/concord-ext-audio),\n[concord-ext-player](https://github.com/narimanized/concord-ext-player),\n[concord-ext-stats](https://github.com/narimanized/concord-ext-stats).\n\n## Installation\n\n#### Via Poetry\n\nConcord uses [Poetry](https://github.com/sdispater/poetry) for it's dependency\nmanagement. You can add Concord to your project using Poetry:\n\n```bash\npoetry add cncrd\n```\n\nPoetry will handle the rest for you.\n\nTake a note, that `cncrd` has no vowels. Concord's and extensions' distribution\nname is`cncrd`.  \n\n#### Via `pip` / other package manager\n\nConcord is hosted on PyPI and can be installed via other package managers:\n\n```bash\npip install cncrd\n```\n\nConcord has a specific requirement - `rewrite` branch of\n[discord.py](https://github.com/Rapptz/discord.py) that is handled by Poetry,\nbut not by other package managers. Take care of installing it too:\n\n```bash\npip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py\n```\n\n#### Development\n\nConcord's development version is located in the `dev` branch, and, in most\ncases, it's a pretty stable to use in case you're a bot developer.\n\n```bash\npoetry add cncrd --git https://github.com/narimanized/concord\n```\n\n## Documentation\n\nI'm really sorry, but there's no online documentation yet.  \nBut. Concord is a small library, the code is well documented, and, with a\nmentioned examples, you can quickly understand everything. Feel free to open an\nissue on GitHub, if you need some help.\n\n## License\n\nMIT.  \nSee LICENSE file for more information.\n",
    'author': 'Nariman Safiulin',
    'author_email': 'woofilee@gmail.com',
    'url': 'https://github.com/narimanized/concord',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
