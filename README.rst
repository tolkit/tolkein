==========================================
Tree of Life Kit of Evolutionary Novelties
==========================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |coveralls|
    * - package
      - |version| |supported-versions| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/tolkein/badge/?style=flat
    :target: https://readthedocs.org/projects/tolkein
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/tolkit/tolkein.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tolkit/tolkein

.. |coveralls| image:: https://coveralls.io/repos/tolkit/tolkein/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/tolkit/tolkein

.. |version| image:: https://img.shields.io/pypi/v/tolkein.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/tolkein

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tolkein.svg
    :alt: Supported versions
    :target: https://pypi.org/project/tolkein

.. |commits-since| image:: https://img.shields.io/github/commits-since/tolkit/tolkein/v0.0.4.svg
    :alt: Commits since latest release
    :target: https://github.com/tolkit/tolkein/compare/v0.0.4...master

.. end-badges


Installation
============

::

    pip install tolkein

You can also install the in-development version with::

    pip install https://github.com/tolkit/tolkein/archive/master.zip


Documentation
=============


https://tolkein.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
