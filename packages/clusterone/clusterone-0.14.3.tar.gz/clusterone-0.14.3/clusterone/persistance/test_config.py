import pytest
from click.exceptions import BadParameter
from coreapi.exceptions import NetworkError

from clusterone.persistance import config
from clusterone import ClusteroneClient


def test_endpoint_slash_and_api(mocker, tmpdir):
    mocker.patch('clusterone.persistance.config.py.path.local', return_value=tmpdir)
    mocker.patch.object(ClusteroneClient, 'download_schema', autospec=True)

    test_config = config.Config()

    test_config.endpoint = "http://elorap.com"

    assert test_config.endpoint == "http://elorap.com/api/"


def test_endpoint_invalid_schema_throw(mocker, tmpdir):
    mocker.patch('clusterone.persistance.config.py.path.local', return_value=tmpdir)
    mocker.patch.object(ClusteroneClient, 'download_schema', autospec=True, return_value=None, side_effect=NetworkError())

    test_config = config.Config()

    with pytest.raises(BadParameter):
        test_config.endpoint = "http://wrongendpoint.com/api/"


@pytest.mark.parametrize(
    "input, result", [
        ("enable", True),
        ("disable", False),
        ("ENABLE", True),
        ("DISABLE", False),
        ("Enable", True),
        ("Disable", False),
        ("eNaBlE", True),
        ("dIsAbLe", False),
    ]
)
def test_tls_valid_values(mocker, input, result, tmpdir):
    mocker.patch('clusterone.persistance.config.py.path.local', return_value=tmpdir)

    test_config = config.Config()

    test_config.tls = input

    assert test_config.tls == result


@pytest.mark.parametrize(
    "input", [
        "turn_on",
        "switch off",
        "enables",
        "disabled",
        "on",
        "off",
        "0",
        "1",
    ]
)
def test_tls_invalid_values(mocker, input, tmpdir):
    mocker.patch('clusterone.persistance.config.py.path.local', return_value=tmpdir)

    test_config = config.Config()

    with pytest.raises(BadParameter):
        test_config.tls = input
