import pytest
from click.testing import CliRunner

from clusterone.clusterone_cli import cli


@pytest.fixture
def notebook(mocker):
    notebook = mocker.Mock()
    notebook.id = '853b9f10-36ce-4de4-b2f8-108d69733b42'
    notebook.owner = 'user'
    notebook.name = 'my-notebook'
    notebook.url = 'http://jupyter.clusterone.com'
    notebook.token = '12345'

    return notebook


def test_should_start_notebook_when_invoked(notebook, mocker):
    mocker.patch('clusterone.ClusteroneClient.__init__')
    notebook_class = mocker.patch('clusterone.just_types.main.JustNotebook')
    notebook_class.from_clusterone.return_value = notebook

    result = CliRunner().invoke(cli, ['start', 'notebook', 'dummy'])

    assert notebook_class.from_clusterone.call_count == 1
    assert notebook.start.call_count == 1
    assert 'Notebook user/my-notebook is running at http://jupyter.clusterone.com/?token=12345' in result.output
