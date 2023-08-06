#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module is provides funcions for dict lists and functions processing
"""
import logging

logger = logging.getLogger(__name__)
import collections
import inspect

def get_default_args(obj):
    first=0
    if ("__init__" in dir(obj)):
        if inspect.isfunction(obj.__init__) or inspect.ismethod(obj.__init__):
            argspec = inspect.getargspec(obj.__init__)
            first = 1
        else:
            argspec = inspect.getargspec(obj)
    else:
        argspec = inspect.getargspec(obj)

    args = argspec.args[first:]
    defaults = argspec.defaults
    ndefaults = len(defaults)
    kwargs_keys = args[-ndefaults:]
    kwargs = collections.OrderedDict(zip(kwargs_keys, defaults))
    args = args[:-ndefaults]
    return args, kwargs

