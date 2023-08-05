import pytest
from coreapi.exceptions import ErrorMessage

from clusterone import ClusteroneClient
from clusterone.business_logic.dataset_commands import LinkGCSDatasetCommand, CreateGCSDatasetCommand


class TestLinkGCSDatasetCommand(object):
    CLIENT_ACTION_PATH = ['datasets', 'link', 'create']

    @pytest.fixture
    def client(self, mocker):
        client = mocker.Mock(spec=ClusteroneClient)

        return client

    def test_should_use_bucket_name_when_bucket_provided(self, client):
        bucket_identifier = 'test-gcs-bucket'

        client.client_action.return_value = {'full_name': 'username/test-gcs-bucket'}

        expected_output = 'username/test-gcs-bucket'
        expected_command_params = {'source': 'gcs',
                                   'display_name': 'test-gcs-bucket',
                                   'http_url_to_repo': '',
                                   'bucket_name': 'test-gcs-bucket'}

        command = LinkGCSDatasetCommand(client, bucket_identifier)
        result = command.execute()

        client.client_action.assert_called_with(self.CLIENT_ACTION_PATH, expected_command_params)
        assert result['output'] == expected_output

    def test_should_extract_name_from_url_when_url_provided(self, client):
        bucket_identifier = 'https://www.googleapis.com/storage/v1/test-gcs-bucket'

        client.client_action.return_value = {'full_name': 'username/test-gcs-bucket'}

        expected_output = 'username/test-gcs-bucket'
        expected_command_params = {'source': 'gcs',
                                   'display_name': 'test-gcs-bucket',
                                   'http_url_to_repo': 'https://www.googleapis.com/storage/v1/test-gcs-bucket',
                                   'bucket_name': ''}

        command = LinkGCSDatasetCommand(client, bucket_identifier)
        result = command.execute()

        client.client_action.assert_called_with(self.CLIENT_ACTION_PATH, expected_command_params)
        assert result['output'] == expected_output

    def test_should_use_custom_display_name_if_provided(self, client):
        bucket_identifier = 'https://www.googleapis.com/storage/v1/test-gcs-bucket'
        custom_display_name = 'a-custom-name'

        client.client_action.return_value = {'full_name': 'username/test-gcs-bucket'}

        expected_output = 'username/test-gcs-bucket'
        expected_command_params = {'source': 'gcs',
                                   'display_name': 'a-custom-name',
                                   'http_url_to_repo': 'https://www.googleapis.com/storage/v1/test-gcs-bucket',
                                   'bucket_name': ''}

        command = LinkGCSDatasetCommand(client, bucket_identifier, custom_display_name)
        result = command.execute()

        client.client_action.assert_called_with(self.CLIENT_ACTION_PATH, expected_command_params)
        assert result['output'] == expected_output

    def test_should_return_errors_when_api_call_fails(self, client):
        bucket_identifier = 'test-gcs-bucket'

        api_exception = ErrorMessage({'bucket_name': ['Bucket name invalid']})
        client.client_action.side_effect = api_exception
        expected_error = 'bucket_name: Bucket name invalid'

        command = LinkGCSDatasetCommand(client, bucket_identifier)
        result = command.execute()

        assert result['errors'] == expected_error


class TestCreateGCSDatasetCommand(object):
    CLIENT_ACTION = ['datasets', 'create']

    @pytest.fixture
    def client(self, mocker):
        client = mocker.Mock(spec=ClusteroneClient)

        return client

    def test_should_send_proper_params_when_client_action_called(self, client):
        bucket_identifier = 'test-gcs-bucket'
        client.client_action.return_value = {'full_name': 'username/test-gcs-bucket',
                                             'bucket_name': 'test-gcs-bucket'}

        expected_output = 'Dataset username/test-gcs-bucket. Use gsutil cp [LOCAL_OBJECT_LOCATION] ' \
                          'gs://test-gcs-bucket to upload data'
        expected_command_params = {'source': 'gcs',
                                   'display_name': 'test-gcs-bucket',
                                   'bucket_name': 'test-gcs-bucket'}

        command = CreateGCSDatasetCommand(client, bucket_identifier)
        result = command.execute()

        client.client_action.assert_called_with(self.CLIENT_ACTION, expected_command_params)
        assert result['output'] == expected_output

    def test_should_return_errors_when_api_call_fails(self, client):
        bucket_identifier = 'test-gcs-bucket'

        api_exception = ErrorMessage({'bucket_name': ['Bucket name invalid']})
        client.client_action.side_effect = api_exception
        expected_error = 'bucket_name: Bucket name invalid'

        command = CreateGCSDatasetCommand(client, bucket_identifier)
        result = command.execute()

        assert result['errors'] == expected_error
