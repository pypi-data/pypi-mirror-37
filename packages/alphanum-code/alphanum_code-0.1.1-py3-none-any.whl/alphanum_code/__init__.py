#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Alphanumeric unique code generator.

This module generates unique consecutive alphanumeric codes of specified size.
A comment can be associated with a code on request.

Requirements:
    - python >= 2.7
    - SQLAchemy
"""


__author__ = "Yec'han Laizet"


import os
from alphanum_code.core import AlphaNumCodeManager


lib_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(lib_path, 'VERSION')) as version_h:
    __version__ = version_h.read().strip()

def version():
    """Get module version."""
    return __version__
