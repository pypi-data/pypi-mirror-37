import os

from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.clusterone_cli import cli
from clusterone.commands.ln.dataset import gitlab
from clusterone.persistance.session import Session


def test_remote_from_dataset_name(mocker):
    gitlab.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={'git_auth_link': "my git auth link", "source": "gitlab"})
    gitlab.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'dataset', 'gitlab', '--dataset-path', 'someuser/someProjectName'])

    gitlab.main.assert_called_with(mocker.ANY, mocker.ANY, "my git auth link")


def test_default_repo_path(mocker):
    gitlab.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={'git_auth_link': "my git auth link", "source": "gitlab"})
    gitlab.main = mocker.Mock()

    CliRunner().invoke(cli, ['ln', 'dataset', 'gitlab', '--dataset-path', 'someuser/someProjectName'])

    gitlab.main.assert_called_with(mocker.ANY, os.getcwd(), mocker.ANY)


def test_user_provided_repo_path(mocker):
    gitlab.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock(return_value={'git_auth_link': "my git auth link", "source": "gitlab"})
    gitlab.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['ln', 'dataset', 'gitlab', '--dataset-path', 'someuser/someProjectName', '-r', '/some/path/to/git/repository'],
        input="")

    gitlab.main.assert_called_with(mocker.ANY, '/some/path/to/git/repository', mocker.ANY)


def test_dataset_aquisition(mocker):
    gitlab.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    gitlab.main = mocker.Mock()

    CliRunner().invoke(
        cli,
        ['ln', 'dataset', 'gitlab', '--dataset-path', 'someuser/someProjectName'])

    ClusteroneClient.get_dataset.assert_called_with("someProjectName", username="someuser")


def test_default_username(mocker):
    gitlab.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    gitlab.main = mocker.Mock()
    mocker.patch.object(Session, 'get', autospec=True, return_value="defaultusername")

    CliRunner().invoke(
        cli,
        ['ln', 'dataset', 'gitlab', '--dataset-path', 'someProjectName'])

    ClusteroneClient.get_dataset.assert_called_with("someProjectName", username="defaultusername")


def test_invalid_dataset_path(mocker):
    gitlab.is_data_on_stdin = mocker.Mock(return_value=False)
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock()
    gitlab.main = mocker.Mock()

    result = CliRunner().invoke(
        cli,
        ['ln', 'dataset', 'gitlab', '--dataset-path', 'elorapmordo/////////xd'], input="")

    # This is a fun way of saying internal Clicks Exception
    assert str(result.exception) == '2'
