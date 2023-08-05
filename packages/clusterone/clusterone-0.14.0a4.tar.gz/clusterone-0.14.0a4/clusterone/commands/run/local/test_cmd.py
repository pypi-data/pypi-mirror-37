import pytest
from clusterone.commands.run.local.cmd import validate_mode, validate_env


@pytest.mark.parametrize(
    'input, result', [
        ("new", False),
        ("current", True),
    ]
)
def test_validate_env(input, result):
    assert validate_env(None, None, input) == result


@pytest.mark.parametrize(
    'input, result', [
        ("single", "single-node"),
        ("distributed", "distributed"),
    ]
)
def test_validate_env(input, result):
    assert validate_mode(None, None, input) == result
