import sys

import importlib
import inspect
import types

import poetry_version
import selenium.webdriver
import splinter
from aioify import aioify

webdrivers = []
for _, module in inspect.getmembers(object=selenium.webdriver):
    # noinspection PyUnresolvedReferences
    if isinstance(module, types.ModuleType):
        webdrivers_module = importlib.import_module(name=module.__name__)
        if hasattr(webdrivers_module, 'webdriver'):
            webdrivers.append(webdrivers_module.webdriver.WebDriver)


__version__ = poetry_version.extract(source_file=__file__)
methods_to_skip = ['full_screen', 'recover_screen']
aiosplinter = aioify(obj=splinter, name=__name__, skip=methods_to_skip + webdrivers, wrap_return_values=True)

sys.modules[__name__] = aiosplinter
from aiosplinter import *
