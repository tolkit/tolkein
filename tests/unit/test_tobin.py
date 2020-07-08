#!/usr/bin/env python3
"""Test functions in tobin."""

import doctest
import unittest

from tolkein import tobin

suite = doctest.DocTestSuite(tobin)


def test_utils_docstrings():
    """Test docstrings in utils module."""
    unittest.TextTestRunner(verbosity=2).run(suite)
