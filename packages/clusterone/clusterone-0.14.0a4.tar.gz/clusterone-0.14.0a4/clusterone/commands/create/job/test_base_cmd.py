from collections import OrderedDict

from clusterone.clusterone_cli import Context
from clusterone.commands.create.job import base_cmd
from clusterone.commands.create.job.base_cmd import _prepare_list_of_datasets
from clusterone.persistance.session import Session


def test_package_manager_aliases(mocker):
    path_to_project_return_value = {'id': "project-id-123456",
                                    "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]),
                                                OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d2')])]}
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_project', return_value=path_to_project_return_value)
    mocker.patch('clusterone.commands.create.job.base_cmd.client')
    mocker.patch('clusterone.commands.create.job.base_cmd.time_limit_to_minutes', return_value=123456)
    kwargs = {'docker_image': 'tensorflow-130',
              'project_path': 'mnist-demo',
              'requirements': None,
              'commit': 'latest',
              'name': 'old-morning-562',
              'command': 'python -m mymodule',
              'package_manager': 'anaconda',
              'description': '',
              'time_limit': 2880,
              'datasets': '', }

    session = Session()
    session.load()
    context = Context(None, session, None)

    result = base_cmd.base(context, kwargs)

    assert result['parameters']['package_manager'] == 'conda'


def test_default_requirement_conda(mocker):
    path_to_project_return_value = {'id': "project-id-123456",
                                    "commits": [OrderedDict([('id', '4a82d16c7995856c7973af38f2f5ba4eac0cd2d1')]),
                                                OrderedDict([('id', '4a82d16c79elorapc7973af38f2f5ba4eac0cd2d1')])]}
    mocker.patch('clusterone.commands.create.job.base_cmd.path_to_project', return_value=path_to_project_return_value)
    mocker.patch('clusterone.commands.create.job.base_cmd.client')
    mocker.patch('clusterone.commands.create.job.base_cmd.time_limit_to_minutes', return_value=123456)
    kwargs = {'docker_image': 'tensorflow-1.3.0',
              'project_path': 'mnist-demo',
              'requirements': None,
              'commit': 'latest',
              'name': 'old-morning-562',
              'command': 'python -m mymodule',
              'package_manager': 'anaconda',
              'description': '',
              'time_limit': 2880,
              'datasets': '', }

    session = Session()
    session.load()
    context = Context(None, session, None)

    result = base_cmd.base(context, kwargs)

    assert result['parameters']['requirements'] == 'requirements.yml'


def test_should_return_an_empty_list_when_datasets_in_kwargs_is_empty():
    kwargs = {'datasets': ''}

    data_sets = _prepare_list_of_datasets('context', kwargs)

    assert data_sets == []


def test_should_return_a_list_of_dicts_when_datasets_in_kwargs_is_not_empty(mocker):
    path_to_dataset_patched = mocker.patch('clusterone.commands.create.job.base_cmd.path_to_dataset',
                                           return_value={'id': 'fake_id'})

    kwargs = {'datasets': 'username/project_name, keton/beton:fake-commit-hash'}

    datasets_list = _prepare_list_of_datasets('fake_context', kwargs)
    fst_dataset = datasets_list[0]
    snd_dataset = datasets_list[1]

    assert fst_dataset == {'dataset': 'fake_id'}
    path_to_dataset_patched.assert_called_with('keton/beton', context='fake_context')
    assert snd_dataset == {'dataset': 'fake_id', 'git_commit_hash': 'fake-commit-hash'}
