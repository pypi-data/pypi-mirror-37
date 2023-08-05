def _sphinx_generator(**kwargs):
    return ".. deprecated :: {deprecated_in}{details}".format(**kwargs)


def _default_generator(**kwargs):
    return "{} since {}.{details}".format(kwargs['current_stage'].name.title(),
                                          kwargs['current_stage'].in_version,
                                          details=kwargs['details'])


def _default_preview_generator(**kwargs):
    if kwargs['next_stage']:
        return "Will be {} in {}.".format(kwargs['next_stage'].name.lower(),
                                          kwargs['next_stage'].in_version)
    else:
        return None


def _default_param_generator(*args):
    return ":parameter: ({}) replaced with ({}).".format(*args)


def generator_preset(docstring=None, warning=None, preview=None, parameter=None):
    return {'docstring': docstring or _default_generator, 'warning': warning or _default_generator,
            'preview': preview or _default_preview_generator, 'parameter': parameter or _default_param_generator}


DEFAULT = generator_preset()
SPHINX = generator_preset(docstring=_sphinx_generator)
