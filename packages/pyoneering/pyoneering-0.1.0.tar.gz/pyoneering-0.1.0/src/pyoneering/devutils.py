import inspect
import warnings
from functools import wraps

from pyoneering.core import Stage, validate_version_identifiers, version
from pyoneering.presets import SPHINX


class DevUtils:
    """This class contains the decorators to annotate objects in a deprecation cycle."""

    def __init__(self, current_version, stages=None, used_in_production=False, preset=None):
        """
        :param current_version:
        :param stages:
            Names for the deprecation cycle - default ['DEPRECATED', 'REMOVED']
        :param used_in_production:
            When used in production decorators get optimized for performance
        :param preset:
            See :func:`pyoneering.presets.generator_presets`
        """
        self.current_version = version.parse(current_version)
        self.used_in_production = used_in_production
        self.stages = stages or ['DEPRECATED', 'REMOVED']
        self.generator = preset or SPHINX

    def _generate_deprecation(self, *version_identifiers):
        stages = list(map(lambda x: Stage(*x), zip(self.stages, map(version.parse, version_identifiers))))

        if not self.used_in_production:
            validate_version_identifiers(stages)

        next_stage = None
        for current_stage in reversed(stages):
            if current_stage.in_version <= self.current_version:
                return {"deprecated_in": version_identifiers[0], "current_stage": current_stage,
                        "next_stage": next_stage}
            next_stage = current_stage
        return None

    def _generate_messages(self, f, **deprecation):
        deprecation['details'] = ' ' + deprecation['details'] if deprecation['details'] else ''
        warning_message = " :: ".join([f.__name__, self.generator['warning'](**deprecation)])
        docstring_message = self.generator['docstring'](**deprecation)
        preview_next_stage = self.generator['preview'](**deprecation)
        if preview_next_stage:
            warning_message = ' '.join([warning_message, preview_next_stage])
            docstring_message = ' '.join([docstring_message, preview_next_stage])
        return docstring_message, warning_message

    def deprecated(self, *version_identifiers, details=None):
        """Decorator to mark a class, function, staticmethod, classmethod or instancemethod as deprecated

        * Inserts information to the docstring describing the current (and next) deprecation stage.
        * Generates a `DeprecationWarning` if the decorator gets called.

        :parameter version_identifiers:
            Specify versions at which the decorated object enters next stage.
        :parameter details:
            Additional information to integrate in docstring
        :exception TypeError:
            If stages not in ascending order.
        """
        deprecation = self._generate_deprecation(*version_identifiers)

        def decorator(f):
            if not deprecation:
                return f

            docstring_message, warning_message = self._generate_messages(f, details=details, **deprecation)

            docstring = f.__doc__.strip() or ""
            docstring = docstring.split('\n', 1)
            docstring.insert(1, docstring_message)
            docstring.insert(1, '\n')
            f.__doc__ = "\n".join(docstring)

            @wraps(f)
            def wrapper(*args, **kwargs):
                warnings.warn(warning_message, DeprecationWarning, stacklevel=3)
                return f(*args, **kwargs)

            return wrapper

        return decorator

    def refactored(self, *version_identifiers, parameter_map, details=None):
        """Decorator to mark keyword arguments as deprecated

        * Replaces old keywords with new ones.
        * Generates a `DeprecationWarning` with if a deprecated keyword argument was passed.

        :param version_identifiers:
            Specify versions at which the decorated object enters next stage.
        :param parameter_map:
            If keyword arguments got renamed, pass a dict with (old_keyword=new_keyword) items.
            Otherwise pass a function with old_keywords and their default values as parameter which
            returns a dict of new_keywords mapped to new values.
        :param details:
            Additional information to integrate in docstring
        :exception TypeError:
            If stages not in ascending order.
        """

        deprecation = self._generate_deprecation(*version_identifiers)

        def decorator(f):
            if not deprecation:
                return f

            docstring_message, warning_message = self._generate_messages(f, details=details, **deprecation)

            if inspect.isfunction(parameter_map):
                old_params = ', '.join(inspect.getfullargspec(parameter_map).args)
                new_params = ', '.join(parameter_map().keys())
                deprecated_params = [self.generator['parameter'](old_params, new_params)]
            elif isinstance(parameter_map, dict):
                deprecated_params = [self.generator['parameter'](k, v) for k, v in parameter_map.items()]
            else:
                raise TypeError("parameter_map needs to be a dict or a function")

            f.__doc__ = "\n\n".join([f.__doc__, '\n\n'.join([docstring_message, '\n'.join(deprecated_params)])])

            @wraps(f)
            def wrapper(*args, **kwargs):
                if inspect.isfunction(parameter_map):
                    signature = inspect.signature(parameter_map)
                    old_kwargs = dict(
                        [(old_key, kwargs[old_key]) for old_key in signature.parameters if old_key in kwargs])
                    new_kwargs = parameter_map(**old_kwargs)
                else:
                    old_kwargs = dict(
                        [(old_key, kwargs[old_key]) for old_key in parameter_map if old_key in kwargs])
                    new_kwargs = dict([(new_key, kwargs[old_key]) for old_key, new_key in parameter_map.items()
                                       if old_key in kwargs])

                for key, value in inspect.signature(f).parameters.items():
                    if key in new_kwargs and new_kwargs[key] is value:
                        del new_kwargs[key]

                for key in old_kwargs.keys():
                    kwargs.pop(key)
                kwargs.update(new_kwargs)

                if old_kwargs:
                    migration_advice = [
                        ', '.join(str(inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, default=value))
                                  for key, value in parameters.items())
                        for parameters in [old_kwargs, new_kwargs]]
                    advice = " Replace ({}) with ({}).".format(*migration_advice)
                else:
                    advice = ""

                warnings.warn("".join([warning_message, advice]), DeprecationWarning, stacklevel=3)
                return f(*args, **kwargs)

            return wrapper

        return decorator
