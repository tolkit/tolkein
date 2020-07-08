#!/usr/bin/env python3
"""Test tolkein entry points."""


def test_tolkein_main():
    """Test main entry point."""
    try:
        from tolkein import main  # pylint: disable=unused-import
        importable = True
    except ImportError:
        importable = False
    assert importable is True
