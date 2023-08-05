import click
import pytest

from clusterone.business_logic.notebook_commands import CreateNotebookCommand, ListNotebooksCommand
from clusterone.just_client import Notebook


class TestCreateNotebookCommand(object):
    @pytest.fixture
    def command_base(self, mocker):
        command_base = mocker.Mock()
        command_base.return_value = {'parameters': {'workers': None},
                                     'meta': {'name': 'my-notebook',
                                              'description': 'My description'}}

        return command_base

    @pytest.fixture
    def notebook_class(self, mocker):
        return mocker.Mock(spec=Notebook)

    @pytest.fixture
    def context(self, mocker):
        return mocker.Mock(spec=click.Context)

    def test_should_return_configured_notebook_when_called(self, command_base, client, notebook_class, context):
        kwargs = {'instance_type': 't2.small'}

        params = {'context': context,
                  'kwargs': kwargs}

        expected_notebook_params = {'name': 'my-notebook',
                                    'description': 'My description',
                                    'mode': CreateNotebookCommand.JOB_MODE,
                                    'workers': {'slug': 't2.small',
                                                'replicas': CreateNotebookCommand.WORKER_REPLICA_COUNT},
                                    'framework': CreateNotebookCommand.JOB_FRAMEWORK}

        command = CreateNotebookCommand(params, command_base, client, notebook_class)
        command.execute()

        notebook_class.assert_called_with(client, expected_notebook_params)
        assert notebook_class.call_count == 1

        command_base.assert_called_with(context, kwargs)
        assert command_base.call_count == 1


class TestListNotebooksCommand(object):
    @pytest.mark.parametrize(("input_entity_data", "expected_output"), [
        (
            {
                "path": "test_user/test_notebook",
                "job_id": "87-457-349-857",
                "repository_owner": "other_user",
                "repository_name": "test_project",
                "git_commit_hash": "954fc994c7e62b2a3259cb367cc6d9b1e25b57b5",
                "status": "Running",
                "latest_snapshot_identifier": "snapshot_name",
            },
            ("test_user/test_notebook", "87-457-349-857", "other_user/test_project:954fc99", "Running", "snapshot_name"),
        ),
        (
            {
                "path": "test_user/test_notebook",
                "job_id": "87-457-349-857",
                "repository_owner": None,
                "repository_name": None,
                "git_commit_hash": None,
                "status": "Running",
                "latest_snapshot_identifier": "snapshot_name",
            },
            ("test_user/test_notebook", "87-457-349-857", "None", "Running", "snapshot_name"),
        ),
        (
            {
                "path": "test_user/test_notebook",
                "job_id": "87-457-349-857",
                "status": "Running",
                "latest_snapshot_identifier": "snapshot_name",
            },
            ("test_user/test_notebook", "87-457-349-857", "None", "Running", "snapshot_name"),
        ),
        (
            {
                "path": "different_test_user/another_test_notebook",
                "job_id": "458-94375-843",
                "repository_owner": "more_user",
                "repository_name": "more_test_project",
                "git_commit_hash": "140e886c6d8ebe4da97509f36d77253693e78296",
                "status": "Starting",
                "latest_snapshot_identifier": "different_snapshot_name",
            },
            ("different_test_user/another_test_notebook", "458-94375-843", "more_user/more_test_project:140e886",
             "Starting", "different_snapshot_name"),
        ),
    ])
    def test_entity_to_row(self, input_entity_data, expected_output):
        assert ListNotebooksCommand._entity_to_row(input_entity_data) == expected_output
