#!/usr/bin/env python3
# encoding: utf-8

from ._public import compile, parse, eval, exec
from .version import __version__
del version

__all__ = ('compile', 'parse', 'eval', 'exec')
