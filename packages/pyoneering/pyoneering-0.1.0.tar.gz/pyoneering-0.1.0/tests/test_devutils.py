import functools
import inspect
import warnings

import pytest
from hypothesis import given
from hypothesis.strategies import none, one_of, text
from pytest import raises

from pyoneering import DevUtils
from pyoneering.presets import generator_preset


def load_decorator(parameter_map, **kwargs):
    module = DevUtils('1.0', stages=['DEPRECATED', 'UNSUPPORTED', 'REMOVED'], **kwargs)
    if parameter_map:
        return functools.partial(module.refactored, parameter_map=parameter_map)
    return module.deprecated


_default_parameter_map = [None, dict(), lambda **_: dict()]


def get_generator(docstring=None, warning=None, preview=None):
    def f(value):
        return lambda *_, **b: value if value else ''

    return generator_preset(docstring=f(docstring), warning=f(warning), preview=f(preview), parameter=f(''))


@pytest.mark.parametrize("parameter_map", _default_parameter_map)
def test_raise_error_if_deprecation_versions_not_ordered(parameter_map):
    with raises(TypeError, message="Expecting TypeError"):
        decorator = load_decorator(parameter_map)

        @decorator('1.0', '1.5', '1.2')
        def func():
            pass


@given(docstring_msg=text(), preview_msg=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", _default_parameter_map)
def test_docstring_message_is_included(parameter_map, docstring_msg, preview_msg):
    decorator = load_decorator(parameter_map, preset=get_generator(docstring=docstring_msg, preview=preview_msg))

    @decorator('0.1')
    def func():
        """summary line"""
        pass

    assert docstring_msg in func.__doc__
    if preview_msg:
        assert preview_msg in func.__doc__


@given(warning_msg=text(), preview_msg=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", _default_parameter_map)
def test_warning_message_is_included(parameter_map, warning_msg, preview_msg):
    with warnings.catch_warnings(record=True) as w:
        decorator = load_decorator(parameter_map, preset=get_generator(warning=warning_msg, preview=preview_msg))

        @decorator('0.1')
        def func():
            """summary line"""
            pass

        func()

        assert DeprecationWarning is w[-1].category
        assert warning_msg in str(w[-1].message)
        if preview_msg:
            assert preview_msg in str(w[-1].message)


@given(docstring_msg=text(), preview_msg=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", _default_parameter_map)
def test_docstring_not_changed_before_deprecated(parameter_map, docstring_msg, preview_msg):
    decorator = load_decorator(parameter_map, preset=get_generator(docstring=docstring_msg, preview=preview_msg))

    @decorator('1.1')
    def func():
        """summary line"""
        pass

    assert func.__doc__ == """summary line"""


@given(warning_msg=text(), preview_msg=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", _default_parameter_map)
def test_no_warning_before_deprecated(parameter_map, warning_msg, preview_msg):
    with warnings.catch_warnings(record=True) as w:
        decorator = load_decorator(parameter_map, preset=get_generator(warning=warning_msg, preview=preview_msg))

        @decorator('1.1')
        def func():
            """summary line"""
            pass

        func()

        assert not w


def _migrate_func(old_kwarg=None):
    return dict(new_kwarg=old_kwarg)


@pytest.mark.parametrize("parameter_map", [dict(old_kwarg='new_kwarg'),
                                           lambda old_kwarg=None: dict(new_kwarg=old_kwarg),
                                           _migrate_func])
def test_function_callable_with_old_kwargs(parameter_map):
    with warnings.catch_warnings(record=True) as w:
        kwarg = '--test--'
        decorator = load_decorator(parameter_map)

        @decorator('0.1')
        def func(arg, new_kwarg=None):
            """summary line"""
            return new_kwarg

        result = func('', old_kwarg=kwarg)

        assert result is kwarg
        assert DeprecationWarning is w[-1].category
        assert "Replace (old_kwarg='--test--') with (new_kwarg='--test--')." in str(w[-1].message)


@pytest.mark.parametrize("parameter_map", [dict(old_kwarg='new_kwarg'),
                                           lambda old_kwarg=None: dict(new_kwarg=old_kwarg),
                                           _migrate_func])
def test_docstring_appended_with_old_kwargs(parameter_map):
    decorator = load_decorator(parameter_map)

    @decorator('0.1')
    def func(arg, new_kwarg=None):
        """summary line"""
        pass

    assert ":parameter: (old_kwarg) replaced with (new_kwarg)." in func.__doc__


@pytest.mark.parametrize("parameter_map", [dict(old_kwarg='new_kwarg'),
                                           lambda old_kwarg=None: dict(new_kwarg=old_kwarg),
                                           _migrate_func])
def test_unchanged_parameters_remain_in_signature(parameter_map):
    decorator = load_decorator(parameter_map)

    @decorator('0.1')
    def func(arg, kwarg1=None, new_kwarg=None):
        """summary line"""
        pass

    parameter_keys = inspect.signature(func).parameters.keys()
    assert "kwarg1" in parameter_keys
    assert "arg" in parameter_keys
