from coreapi.exceptions import ErrorMessage

from clusterone.business_logic.providers import Providers
from clusterone.just_client.main import parse_api_error_messages


class LinkGCSDatasetCommand:
    CLIENT_ACTION = ['datasets', 'link', 'create']

    def __init__(self, client, bucket_identifier, custom_display_name=None):
        self.client = client
        self.bucket_identifier = bucket_identifier
        self.custom_display_name = custom_display_name
        self._preprocess_params()

    def execute(self):
        errors = None
        params = {'source': Providers.GCS,
                  'display_name': self._get_display_name(),
                  'http_url_to_repo': self.http_url_to_repo,
                  'bucket_name': self.bucket_name}
        try:
            result = self.client.client_action(self.CLIENT_ACTION, params)
            output = result['full_name']
        except ErrorMessage as e:
            errors = parse_api_error_messages(e)
            output = ''

        return {'errors': errors,
                'data': params,
                'output': output}

    def _preprocess_params(self):
        if self.bucket_identifier.startswith('http'):
            bucket_url_split = self.bucket_identifier.split('/')
            self.display_name = bucket_url_split[-1]
            self.bucket_name = ''
            self.http_url_to_repo = self.bucket_identifier
        else:
            self.display_name = self.bucket_identifier
            self.bucket_name = self.bucket_identifier
            self.http_url_to_repo = ''

    def _get_display_name(self):
        if self.custom_display_name:
            return self.custom_display_name

        return self.display_name


class CreateGCSDatasetCommand:
    CLIENT_ACTION = ['datasets', 'create']
    SUCCESS_MESSAGE = 'Dataset {}. Use gsutil cp [LOCAL_OBJECT_LOCATION] gs://{} to upload data'

    def __init__(self, client, bucket_identifier):
        self.client = client
        self.bucket_identifier = bucket_identifier

    def execute(self):
        errors = None
        params = {'source': Providers.GCS,
                  'display_name': self.bucket_identifier,
                  'bucket_name': self.bucket_identifier}

        try:
            result = self.client.client_action(self.CLIENT_ACTION, params)
            output = self.SUCCESS_MESSAGE.format(result['full_name'], result['bucket_name'])
        except ErrorMessage as e:
            errors = parse_api_error_messages(e)
            output = ''

        return {'errors': errors,
                'data': params,
                'output': output}
