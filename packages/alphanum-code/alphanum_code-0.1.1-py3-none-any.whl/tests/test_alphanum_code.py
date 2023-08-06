#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test AlphanumCOde.

Usage:
    python -m pytest tests/

"""

import datetime
import pytest
import os
from alphanum_code import AlphaNumCodeManager

INIT_CODE = "52Z9Z"


@pytest.fixture(scope="module")
def coder():
    manager = AlphaNumCodeManager("sqlite:///tests/codes.sqlite", code_size=5, init_code=INIT_CODE)
    yield manager
    os.remove("tests/codes.sqlite")


def test_init_code(coder):
    code = coder.next_code("init code test")
    assert code == INIT_CODE


def test_next_code(coder):
    coder.next_code()
    code = coder.next_code("next code test")
    assert code == "52ZA1"
