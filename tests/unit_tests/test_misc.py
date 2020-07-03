#!/usr/bin/env python3
"""Test functions in misc."""

import doctest
import unittest

from tolkein import misc

suite = doctest.DocTestSuite(misc)


def test_misc_docstrings():
    """Test docstrings in misc module."""
    unittest.TextTestRunner(verbosity=2).run(suite)
