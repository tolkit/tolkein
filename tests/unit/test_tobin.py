#!/usr/bin/env python3
"""Test functions in tobin."""

import doctest
import unittest

from tolkein import tobin

suite = doctest.DocTestSuite(tobin)


def test_tobin_docstrings():
    """Test docstrings in tobin module."""
    unittest.TextTestRunner(verbosity=3).run(suite)
