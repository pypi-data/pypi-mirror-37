import pytest
from packaging import version
from pytest import raises

from pyoneering.core import Stage, create_stage_information, generate_version_identifiers, validate_version_identifiers


@pytest.mark.parametrize("stage_names, version_identifiers, expected_stages", [
    (['DEPRECATED'], ['0.1.0'], [Stage('DEPRECATED', version.parse('0.1.0'))]),
    (['DEPRECATED', 'UNSUPPORTED'], ['0.1.0', '1.0.3'],
     [Stage('DEPRECATED', version.parse('0.1.0')), Stage('UNSUPPORTED', version.parse('1.0.3'))])
])
def test_creates_stages(stage_names, version_identifiers, expected_stages):
    stages = generate_version_identifiers(stage_names, version_identifiers)

    assert stages == expected_stages


@pytest.mark.parametrize("stages", [
    ([Stage('DEPRECATED', version.parse('0.1.0'))]),
    ([Stage('DEPRECATED', version.parse('0.1.0')), Stage('UNSUPPORTED', version.parse('1.0.3'))]),
    ([Stage('DEPRECATED', version.parse('1.0.e')), Stage('UNSUPPORTED', version.parse('1.0.f'))])
])
def test_validate_correct_stages_without_error(stages):
    validate_version_identifiers(stages)


@pytest.mark.parametrize("stages", [
    ([Stage('DEPRECATED', version.parse('0.1.0')), Stage('UNSUPPORTED', version.parse('0.1.0'))]),
    ([Stage('DEPRECATED', version.parse('2.1.0')), Stage('UNSUPPORTED', version.parse('1.0.3'))])
])
def test_validate_stages_with_error(stages):
    with raises(TypeError):
        validate_version_identifiers(stages)


@pytest.mark.parametrize("current_version", ['0.9', '1.0', '1.5.3'])
@pytest.mark.parametrize("stages", [['0.9', '1.0', '1.5.3']])
def test_create_stage_information(current_version, stages):
    _current_version = version.parse(current_version)
    _stages = [Stage(i, version.parse(x)) for i, x in enumerate(stages)]

    information = create_stage_information(_current_version, _stages)

    assert information['deprecated_in'] == version.parse('0.9')
    assert information['current_stage'].in_version <= _current_version
    if current_version != '1.5.3':
        assert information['next_stage'].in_version > _current_version
        assert information['current_stage'].name + 1 == information['next_stage'].name
    else:
        assert information['next_stage'] is None
