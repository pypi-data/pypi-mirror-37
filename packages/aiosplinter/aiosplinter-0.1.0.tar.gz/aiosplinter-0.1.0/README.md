# aiosplinter - asynchronous splinter wrapper Python library
Asynchronous [splinter](https://github.com/cobrateam/splinter) wrapper Python library

## Installation
To install from [PyPI](https://pypi.org/project/aiosplinter/) run:
```shell
$ pip install aiosplinter
```

## Usage
See `splinter` [documentation](https://splinter.readthedocs.io/en/latest/), because `aiosplinter` uses the same API as 
`splinter` with 2 exceptions:
1. All functions are converted to coroutines, that means you have to add `await` keyword before all function calls.
2. To asynchronously create classes from `aiosplinter` use static method `create`.

Example (open https://google.com with `chrome`, make screenshot and show it in default browser):
```python
#!/usr/bin/env python

import asyncio
import webbrowser
from pathlib import Path

import aiosplinter


browser_name = 'chrome'
browser = asyncio.run(aiosplinter.Browser(driver_name=browser_name))
url = 'https://google.com'
asyncio.run(browser.visit(url=url))
screenshot_filename_base = str(Path('~/google.com_screenshot_').expanduser())
screenshot_filename = asyncio.run(browser.screenshot(name=screenshot_filename_base, full=True))
webbrowser.open(url=f'file://{screenshot_filename}')
asyncio.run(browser.quit())
```
