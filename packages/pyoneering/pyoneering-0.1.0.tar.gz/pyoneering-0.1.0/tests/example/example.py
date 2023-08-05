import sys
import warnings

from tests.example.utils import deprecated, refactored


@deprecated('0.6', '1.8')
class DeprecatedClass:
    """Example of a deprecated class."""
    pass


@deprecated('0.2', '0.8', details='Use new method instead')
def deprecated_method():
    """Example of a deprecated method."""
    pass


@refactored('0.4', '2.0', parameter_map={'old_kwarg2': 'new_kwarg1'})
def renamed_parameter(kwarg1=5, new_kwarg1=False):
    """Example of a method with changed signature."""
    pass


def _merged_parameters(old_kwarg2=True, old_kwarg3=False):
    if not old_kwarg2 and not old_kwarg3:
        new_kwarg1 = 'cat-1'
    elif old_kwarg2 and not old_kwarg3:
        new_kwarg1 = 'cat-2'
    else:
        new_kwarg1 = 'error'

    return dict(new_kwarg1=new_kwarg1)


@refactored('0.4', parameter_map=_merged_parameters)
def merged_parameter(kwarg1=5, new_kwarg1='error'):
    """Example of a method with changed signature."""
    pass


if 'sphinx' in sys.modules:
    def document_warning(runnable, **kwargs):
        warnings.filterwarnings('once')
        with warnings.catch_warnings(record=True) as w:
            runnable(**kwargs)
            warning = '.\nReplace'.join(str(w[-1].message).split('. Replace'))
            runnable.__doc__ += ("\n"
                                 "\n"
                                 ">>> {}({})  # Generates warning:\n"
                                 "{}").format(runnable.__name__,
                                              ', '.join(['{}={}'.format(a, b) for a, b in kwargs.items()]), warning)

    document_warning(DeprecatedClass)
    document_warning(deprecated_method)
    document_warning(renamed_parameter, old_kwarg2=True)
    document_warning(merged_parameter, old_kwarg2=True)
    document_warning(merged_parameter, old_kwarg2=False, old_kwarg3=True)
