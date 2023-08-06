# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiosplinter']

package_data = \
{'': ['*']}

install_requires = \
['aioify', 'poetry-version', 'splinter>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'aiosplinter',
    'version': '0.1.0',
    'description': 'Asynchronous splinter wrapper Python library',
    'long_description': "# aiosplinter - asynchronous splinter wrapper Python library\nAsynchronous [splinter](https://github.com/cobrateam/splinter) wrapper Python library\n\n## Installation\nTo install from [PyPI](https://pypi.org/project/aiosplinter/) run:\n```shell\n$ pip install aiosplinter\n```\n\n## Usage\nSee `splinter` [documentation](https://splinter.readthedocs.io/en/latest/), because `aiosplinter` uses the same API as \n`splinter` with 2 exceptions:\n1. All functions are converted to coroutines, that means you have to add `await` keyword before all function calls.\n2. To asynchronously create classes from `aiosplinter` use static method `create`.\n\nExample (open https://google.com with `chrome`, make screenshot and show it in default browser):\n```python\n#!/usr/bin/env python\n\nimport asyncio\nimport webbrowser\nfrom pathlib import Path\n\nimport aiosplinter\n\n\nbrowser_name = 'chrome'\nbrowser = asyncio.run(aiosplinter.Browser(driver_name=browser_name))\nurl = 'https://google.com'\nasyncio.run(browser.visit(url=url))\nscreenshot_filename_base = str(Path('~/google.com_screenshot_').expanduser())\nscreenshot_filename = asyncio.run(browser.screenshot(name=screenshot_filename_base, full=True))\nwebbrowser.open(url=f'file://{screenshot_filename}')\nasyncio.run(browser.quit())\n```\n",
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'url': 'https://github.com/rominf/aiosplinter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
