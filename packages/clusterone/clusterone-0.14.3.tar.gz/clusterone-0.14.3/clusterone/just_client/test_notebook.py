from click.testing import CliRunner
from coreapi.document import Error
from coreapi.exceptions import ErrorMessage
from pytest import raises

from clusterone import client
from clusterone.client_exceptions import _NonExistantNotebook, NonExistantNotebook, ClusteroneException
from clusterone.clusterone_cli import cli
from clusterone.just_client.types import TaskStatus
from clusterone.mocks import NOTEBOOK_JOB_CONFIGURATION, NOTEBOOK_API_RESPONSE
from .notebook import Notebook, NotebookPath


def test_existing_from_uuid(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.return_value = NOTEBOOK_API_RESPONSE

    target = Notebook._from_data(client, NOTEBOOK_API_RESPONSE)

    notebook = Notebook.from_clusterone(mock_client, "853b9f10-36ce-4de4-b2f8-108d69733b42")
    args, kwargs = mock_client.client_action.call_args

    assert notebook == target
    assert args[0] == ['notebooks', 'read']
    assert kwargs['params'] == {
        'job_id': "853b9f10-36ce-4de4-b2f8-108d69733b42",
    }


def test_existing_from_path(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.return_value = NOTEBOOK_API_RESPONSE

    target = Notebook._from_data(mock_client, NOTEBOOK_API_RESPONSE)

    notebook = Notebook.from_clusterone(mock_client, "dummy/winter-leaf-119")
    args, kwargs = mock_client.client_action.call_args

    assert notebook == target
    assert args[0] == ['notebook_by_name', 'read']
    assert kwargs['params'] == {
        "display_name": "winter-leaf-119",
        "username": "dummy",
    }


def test_existing_from_path_without_username(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.return_value = NOTEBOOK_API_RESPONSE
    mock_client.username = "dummy"

    Notebook.from_clusterone(mock_client, "winter-leaf-119")
    args, kwargs = mock_client.client_action.call_args

    assert kwargs['params']['username'] == "dummy"


def test_failed_acquisition_by_name(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.side_effect = ErrorMessage(
        Error(title='404 Not Found', content={'detail': 'Notebook not found'}))

    with raises(NonExistantNotebook):
        Notebook.from_clusterone(mock_client, "dummy/winter-leaf-119")


def test_failed_acquisition_by_id(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.side_effect = ErrorMessage(
        Error(title='404 Not Found', content={'detail': 'Notebook not found'}))

    with raises(_NonExistantNotebook):
        Notebook.from_clusterone(mock_client, "853b9f10-36ce-4de4-b2f8-108d69733b42")


def test_new(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.return_value = NOTEBOOK_API_RESPONSE

    target = Notebook._from_data(mock_client, NOTEBOOK_API_RESPONSE)

    assert Notebook(mock_client, NOTEBOOK_JOB_CONFIGURATION) == target

    args, kwargs = mock_client.client_action.call_args
    assert args[0] == ['notebooks', 'create']
    assert kwargs['params'] == {
        'display_name': 'snowy-surf-115',
        'description': '',
        'parameters': NOTEBOOK_JOB_CONFIGURATION,
        'datasets_set': [],
    }


def test_failed_creation(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.side_effect = ErrorMessage(Error(title='400 Bad Request', content={
        ' messages': [' Fields username and display_name must make a unique set.']}))
    with raises(ClusteroneException):
        Notebook(mock_client, NOTEBOOK_JOB_CONFIGURATION)


def test_initialisation(mocker):
    mock_client = mocker.Mock()
    test_notebook = Notebook.__new__(Notebook)
    test_notebook._initialize(mock_client, NOTEBOOK_API_RESPONSE)

    assert test_notebook.id == "853b9f10-36ce-4de4-b2f8-108d69733b42"
    assert test_notebook.url == "http://853b9f10-36ce-4de4-b2f8-108d69733b42.jupyter.v2.clusterone.com"
    assert test_notebook.status == TaskStatus.created
    assert test_notebook.token == '85c88d21-fb18-42be-8a1a-f73da4585a02'


def test_from_data_constructor(mocker):
    mock_client = mocker.Mock()
    template = Notebook.__new__(Notebook)
    template._initialize(mock_client, NOTEBOOK_API_RESPONSE)

    target = Notebook._from_data(mock_client, NOTEBOOK_API_RESPONSE)

    assert template == target


def test_starting(mocker):
    mock_client = mocker.Mock()
    test_notebook = Notebook._from_data(mock_client, NOTEBOOK_API_RESPONSE)

    test_notebook.start(mock_client)

    assert test_notebook.status == TaskStatus.started
    args, kwargs = mock_client.client_action.call_args
    assert args[0] == ['notebooks', 'start']
    assert kwargs['params'] == {
        'job_id': '853b9f10-36ce-4de4-b2f8-108d69733b42',
    }


def test_stopping(mocker):
    mock_client = mocker.Mock()
    test_notebook = Notebook._from_data(mock_client, NOTEBOOK_API_RESPONSE)

    test_notebook.stop(mock_client)

    assert test_notebook.status == TaskStatus.stopped
    args, kwargs = mock_client.client_action.call_args
    assert args[0] == ['notebooks', 'stop']
    assert kwargs['params'] == {
        'job_id': '853b9f10-36ce-4de4-b2f8-108d69733b42',
    }


def test_repr(mocker):
    mock_client = mocker.Mock()
    test_notebook = Notebook._from_data(mock_client, NOTEBOOK_API_RESPONSE)

    assert repr(test_notebook) == "Notebook(<client_instance>, '853b9f10-36ce-4de4-b2f8-108d69733b42')"


def test_parsing_notebook_path():
    assert Notebook._parse_notebook_path("username/notebook") == NotebookPath(username="username", notebook_name="notebook")
    assert Notebook._parse_notebook_path("notebook") == NotebookPath(username=None, notebook_name="notebook")

    with raises(ValueError):
        Notebook._parse_notebook_path("keton/keton/keton/keton")

    with raises(ValueError):
        Notebook._parse_notebook_path("/")


def test_should_create_notebook_when_there_is_no_git_commit_hash_in_configuration(mocker):
    mock_client = mocker.Mock()
    mock_client.client_action.return_value = NOTEBOOK_API_RESPONSE

    configuration = {'name': 'keton',
                     'description': 'keton keton',
                     'datasets_set': 'keton dataset',
                     'repository': 'keton',
                     }

    _ = Notebook(mock_client, configuration)

    params = {
        'display_name': configuration['name'],
        'description': configuration['description'],
        'parameters': configuration,
        'datasets_set': configuration['datasets_set'],
        'repository': 'keton'
    }
    mock_client.client_action.assert_called_once_with(['notebooks', 'create'], params=params)


def test_should_post_data_with_valid_git_commit_hash_when_was_provided_in_cli(mocker):
    _send_create_request_patched = mocker.patch('clusterone.just_client.notebook.Notebook._send_create_request',
                                                return_value=NOTEBOOK_API_RESPONSE)
    mocker.patch('clusterone.just_client.notebook.Notebook._initialize')
    mocker.patch('clusterone.just_client.ClusteroneClient.get_project',
                 return_value={'id': 'fake_id'})

    expected_params = {
        'display_name': 'keton',
        'description': '',
        'parameters': {
            'command': 'python -m main',
            'package_manager': 'pip',
            'requirements': 'requirements.txt',
            'time_limit': 2880,
            'repository': 'fake_id',
            'framework': {
                'slug': 'jupyter',
            },
            'datasets_set': [],
            'git_commit_hash': 'fake-git-commit-hash',
            'mode': 'single',
            'workers': {
                'slug': 't2.small',
                'replicas': 1,
            },
            'name': 'keton',
            'description': '',
        },
        'datasets_set': [],
        'repository': 'fake_id',
        'git_commit_hash': 'fake-git-commit-hash',
    }

    CliRunner().invoke(cli, [
        'create',
        'notebook',
        '--name', 'keton',
        '--project', 'keton/keton_project',
        '--commit', 'fake-git-commit-hash',
    ])

    _send_create_request_patched.assert_called_with(client, expected_params)


def test_should_post_data_without_git_commit_hash_when_project_was_provided_but_hash_was_not(mocker):
    _send_create_request_patched = mocker.patch('clusterone.just_client.notebook.Notebook._send_create_request',
                                                return_value=NOTEBOOK_API_RESPONSE)
    mocker.patch('clusterone.just_client.notebook.Notebook._initialize')
    mocker.patch('clusterone.just_client.ClusteroneClient.get_project',
                 return_value={'id': 'fake_id'})

    expected_params = {
        'display_name': 'keton',
        'description': '',
        'parameters': {
            'command': 'python -m main',
            'package_manager': 'pip',
            'requirements': 'requirements.txt',
            'time_limit': 2880,
            'repository': 'fake_id',
            'framework': {
                'slug': 'jupyter',
            },
            'datasets_set': [],
            'mode': 'single',
            'workers': {
                'slug': 't2.small',
                'replicas': 1,
            },
            'name': 'keton',
            'description': '',
        },
        'datasets_set': [],
        'repository': 'fake_id',
    }

    CliRunner().invoke(cli, [
        'create',
        'notebook',
        '--name', 'keton',
        '--project', 'keton/keton_project',
    ])

    _send_create_request_patched.assert_called_with(client, expected_params)


def test_should_post_valid_data_when_many_optional_parameters_were_used(mocker):
    _send_create_request_patched = mocker.patch('clusterone.just_client.notebook.Notebook._send_create_request',
                                                return_value=NOTEBOOK_API_RESPONSE)
    mocker.patch('clusterone.just_client.notebook.Notebook._initialize')
    mocker.patch('clusterone.just_client.ClusteroneClient.get_project',
                 return_value={'id': 'fake_id'})
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_project', return_value={'id': 'fake_id'})
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_dataset',
                 return_value={'id': '44ebece9-1052-423b-a636-279dd1fc1580'})

    expected_params = {
        'display_name': 'keton',
        'description': 'some description',
        'parameters': {
            'command': 'python -m some_module_name',
            'package_manager': 'pip',
            'requirements': 'requirements.txt',
            'time_limit': 2881,
            'repository': 'fake_id',
            'framework': {
                'slug': 'jupyter',
            },
            'datasets_set': [
                {
                    'dataset': '44ebece9-1052-423b-a636-279dd1fc1580',
                },
            ],
            'git_commit_hash': 'fake-git-commit-hash',
            'mode': 'single',
            'workers': {
                'slug': 'p2.xlarge',
                'replicas': 1,
            },
            'name': 'keton',
            'description': 'some description',
        }, 'datasets_set': [
            {
                'dataset': '44ebece9-1052-423b-a636-279dd1fc1580',
            },
        ],
        'repository': 'fake_id',
        'git_commit_hash': 'fake-git-commit-hash',
    }

    CliRunner().invoke(cli, [
        'create',
        'notebook',
        '--name', 'keton',
        '--commit', 'fake-git-commit-hash',
        '--datasets', 'some/dataset',
        '--command', 'python -m some_module_name',
        '--docker-image', 'tensorflow-1.3.0-cpu-py36',
        '--package-manager', 'pip',
        '--requirements', 'requirements.txt',
        '--time-limit', '48h01m',
        '--description', 'some description',
        '--gpu-count', '4',
        '--project', 'some/project',
        '--instance-type', 'p2.xlarge',
    ])

    _send_create_request_patched.assert_called_with(client, expected_params)


def test_should_send_proper_request_when_start_notebook_command_with_uuid_was_used(mocker):
    client_cmd_patched = mocker.patch('clusterone.commands.start.notebook.cmd.client')
    client_patched = mocker.patch('clusterone.just_types.main.client')
    client_patched.client_action.return_value = {'job_id': 'some-job-id',
                                                 'notebook_url': 'some_url',
                                                 'status': 'started',
                                                 'display_name': 'some-name',
                                                 'parameters': {'token': 'some-token'}}

    result = CliRunner().invoke(cli, ['start', 'notebook', 'some-job-id'])
    print(result.output)

    client_cmd_patched.client_action.assert_called_with(['notebooks', 'start'], params={'job_id': 'some-job-id'})


def test_should_send_proper_request_when_stop_notebook_command_with_uuid_was_used(mocker):
    client_cmd_patched = mocker.patch('clusterone.commands.stop.notebook.cmd.client')
    client_patched = mocker.patch('clusterone.just_types.main.client')
    client_patched.client_action.return_value = {'job_id': 'some-job-id',
                                                 'notebook_url': 'some_url',
                                                 'status': 'started',
                                                 'display_name': 'some-name',
                                                 'parameters': {'token': 'some-token'}}

    result = CliRunner().invoke(cli, ['stop', 'notebook', 'some-job-id'])
    print(result.output)

    client_cmd_patched.client_action.assert_called_with(['notebooks', 'stop'], params={'job_id': 'some-job-id'})
