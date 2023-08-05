========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-pyoneering/badge/?style=flat
    :target: https://readthedocs.org/projects/python-pyoneering
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/FHaase/python-pyoneering.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/FHaase/python-pyoneering

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/FHaase/python-pyoneering?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/FHaase/python-pyoneering

.. |requires| image:: https://requires.io/github/FHaase/python-pyoneering/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/FHaase/python-pyoneering/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/github/FHaase/python-pyoneering/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/FHaase/python-pyoneering?branch=master

.. |codecov| image:: https://codecov.io/github/FHaase/python-pyoneering/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/FHaase/python-pyoneering

.. |landscape| image:: https://landscape.io/github/FHaase/python-pyoneering/master/landscape.svg?style=flat
    :target: https://landscape.io/github/FHaase/python-pyoneering/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/pyoneering.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pyoneering

.. |commits-since| image:: https://img.shields.io/github/commits-since/FHaase/python-pyoneering/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/FHaase/python-pyoneering/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pyoneering.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pyoneering

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pyoneering.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pyoneering

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pyoneering.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pyoneering


.. end-badges

Decorators for deprecating and refactoring

* Free software: Apache Software License 2.0

Installation
============

::

    pip install pyoneering

Documentation
=============


https://python-pyoneering.readthedocs.io/


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
