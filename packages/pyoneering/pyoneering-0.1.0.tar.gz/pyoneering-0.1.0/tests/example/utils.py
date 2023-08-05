from tests.example import __version__

from pyoneering import DevUtils

_module = DevUtils(__version__)
deprecated, refactored = _module.deprecated, _module.refactored
