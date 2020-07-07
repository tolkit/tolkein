#!/usr/bin/env python3
"""Test functions in misc."""

import doctest
import unittest

from tolkein import utils

suite = doctest.DocTestSuite(utils)


def test_utils_docstrings():
    """Test docstrings in utils module."""
    unittest.TextTestRunner(verbosity=2).run(suite)
