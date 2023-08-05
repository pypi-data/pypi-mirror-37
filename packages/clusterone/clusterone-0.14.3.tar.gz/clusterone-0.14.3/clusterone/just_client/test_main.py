from clusterone import ClusteroneClient


def test_lazy_schema_acquisition(mocker):
    """
    ClusteroneClient should NOT download schema on initialisation
    """

    mocker.spy(ClusteroneClient, 'download_schema')

    client = ClusteroneClient(api_url="https://not-real-domain.test/api")

    assert not client.download_schema.called

