===============
Getting started
===============

Configuration
=============

In order to provide a module-wide configuration for the decorators :func:`deprecated` and
:func:`refactored` include the following code-snippet in your module.

.. _default-configuration:
.. literalinclude:: /../tests/example/utils.py

Then these functions are accessible from anywhere in your module.

.. literalinclude:: /../tests/example/example.py
    :lines: 4

Examples
========

The examples are generated with :attr:`__version__='1.0'`.

deprecated class
----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: DeprecatedClass

.. autoclass:: tests.example.DeprecatedClass

deprecated method
-----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: deprecated_method

.. automethod:: tests.example.deprecated_method

renamed parameter
-----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: renamed_parameter

.. automethod:: tests.example.renamed_parameter

merged parameter
----------------

.. literalinclude:: /../tests/example/example.py
    :pyobject: _merged_parameters
.. literalinclude:: /../tests/example/example.py
    :pyobject: merged_parameter

.. automethod:: tests.example.merged_parameter
