import pytest

from clusterone import ClusteroneClient


@pytest.fixture
def client(mocker):
    return mocker.Mock(spec=ClusteroneClient)
