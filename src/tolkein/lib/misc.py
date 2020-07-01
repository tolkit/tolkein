#!/usr/bin/env python3

"""
Miscellaneous functions.

Simple tests are included in docstrings and run using doctest.

Further tests are implemented in a separate file using pytest
(see tests/unit_tests/test_misc.py).
"""

import math


def bin_hr_simple(value):
    r"""
    Place values in human readable bins.

    >>> bin_hr_simple(123456789)
    '200M'

    >>> bin_hr_simple(56789012234)
    '100G'

    >>> bin_hr_simple(567.89)
    '1k'

    >>> bin_hr_simple(21)
    '30'

    >>> bin_hr_simple(0.6)
    '1'

    >>> bin_hr_simple(-1234567)
    '-2M'
    """
    thousands = ['', 'k', 'M', 'G']
    start_digits = [1, 2, 3, 5, 10]
    # Check sign
    sign = 1
    if value < 0:
        value = abs(value)
        sign = -1
    # Check order of magnitude
    order = int(math.floor(math.log10(abs(value))))
    # Get first digit
    first = value / pow(10, order)
    # Find bin
    for digit in start_digits:
        if first < digit:
            initial = digit
            if initial == 10:
                order += 1
                initial = 1
            break
    # Count thousands
    mag = order // 3
    # Count additional orders of magnitude
    order %= 3
    # Set return value
    value = sign * initial * pow(10, order)
    return "%d%s" % (value, thousands[mag])


if __name__ == '__main__':
    # Run inline tests
    import doctest
    doctest.testmod()
