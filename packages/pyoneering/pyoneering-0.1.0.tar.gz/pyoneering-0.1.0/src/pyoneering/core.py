from collections import namedtuple

from packaging import version

Stage = namedtuple('Stage', ['name', 'in_version'])


def generate_version_identifiers(stage_names, version_identifier):
    return list(map(lambda x: Stage(*x), zip(stage_names, map(version.parse, version_identifier))))


def validate_version_identifiers(stages):
    for current_stage, next_stage in zip(stages, stages[1:]):
        if current_stage.in_version >= next_stage.in_version:
            raise TypeError("Don't schedule {} in {} after {} in {}."
                            .format(current_stage.name.lower(), current_stage.in_version,
                                    next_stage.name.lower(), next_stage.in_version))


def create_stage_information(current_version, stages):
    next_stage = None
    for current_stage in reversed(stages):
        if current_stage.in_version <= current_version:
            return {"deprecated_in": stages[0].in_version, "current_stage": current_stage, "next_stage": next_stage}
        next_stage = current_stage
    return None
