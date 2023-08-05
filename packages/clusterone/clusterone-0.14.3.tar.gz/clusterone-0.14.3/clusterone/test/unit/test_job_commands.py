from collections import defaultdict

import pytest

import clusterone
from clusterone import ClusteroneClient
from clusterone.business_logic.job_commands import CreateSingleJobCommand, CreateDistributedJobCommand, StartJobCommand, \
    RunJobCommand, relative_job_path


@pytest.fixture
def client_create_job(mocker):
    mock = mocker.Mock(spec=ClusteroneClient)

    mock.create_job.return_value = {
        "job_id": "someUUID",
        "repository_name": "sample_project",
        "display_name": "sample_job",
    }
    mock.username = "#"

    return mock


@pytest.fixture
def client_start_job(mocker):
    mock = mocker.Mock(spec=ClusteroneClient)

    mock.start_job.return_value = {
        "path": "sample_user/sample_project/sample_job",
    }
    mock.username = "sample_user"

    return mock


@pytest.fixture
def kwargs():
    sample_kwargs = defaultdict(lambda: None)

    sample_kwargs["ps_replicas"] = 1
    sample_kwargs["worker_replicas"] = 2

    return sample_kwargs


@pytest.mark.parametrize("current_user_username, absolute_job_path, expected_output", [
    ("user", "user/project/job", "project/job"),
    ("another-user", "another-user/different_project/different_job", "different_project/different_job"),
    ("user", "someone/project/job", "someone/project/job"),
    ("user", "someone-else/project/job", "someone-else/project/job"),
])
def test_relative_job_path(absolute_job_path, current_user_username, expected_output):
    assert relative_job_path(absolute_job_path, current_user_username) == expected_output


class TestCreateJobCommand(object):
    # TODO: Write those tests - see `clusterone/create/job/test_base_cmd` for inspiration
    pass


class TestCreateDistributedJobCommand(object):
    def test_returns_output_relative_job_path(self, client_create_job, kwargs):
        command = CreateDistributedJobCommand(client=client_create_job, kwargs=kwargs)
        command_result = command.execute()

        assert command_result["output"] == "sample_project/sample_job"

    def test_mode_is_distributed(self, client_create_job, kwargs):
        command = CreateDistributedJobCommand(client=client_create_job, kwargs=kwargs)
        command.execute()

        _, call_kwargs = client_create_job.create_job.call_args

        assert call_kwargs["parameters"]["mode"] == "distributed"

    def test_when_passed_pytorch_raises_value_error(self, client_create_job, kwargs):
        kwargs["docker_image"] = "pytorch-1.0.0"

        command = CreateDistributedJobCommand(client=client_create_job, kwargs=kwargs)

        with pytest.raises(ValueError):
            command.execute()

    @pytest.mark.parametrize("test_input_worker_type,test_result_worker_type", [
        ("test_machine_slug",) * 2,
        ("other_machine_slug",) * 2,
    ])
    @pytest.mark.parametrize("test_input_ps_type,test_result_ps_type", [
        ("test_machine_slug",) * 2,
        ("other_machine_slug",) * 2,
    ])
    @pytest.mark.parametrize("test_input_worker_replicas,test_result_worker_replicas", [
        (1,) * 2,
        (8,) * 2,
    ])
    @pytest.mark.parametrize("test_input_ps_replicas,test_result_ps_replicas", [
        (1,) * 2,
        (8,) * 2,
    ])
    def test_when_workers_and_ps_are_passed_then_are_present_in_api_call(self, client_create_job, kwargs, test_input_worker_type,
                                                                         test_result_worker_type,
                                                                         test_input_ps_type, test_result_ps_type,
                                                                         test_input_worker_replicas,
                                                                         test_result_worker_replicas,
                                                                         test_input_ps_replicas,
                                                                         test_result_ps_replicas):
        kwargs.update({"worker_type": test_input_worker_type,
                       "worker_replicas": test_input_worker_replicas,
                       "ps_type": test_input_ps_type,
                       "ps_replicas": test_input_ps_replicas})

        command = CreateDistributedJobCommand(client=client_create_job, kwargs=kwargs)
        command.execute()

        _, call_kwargs = client_create_job.create_job.call_args

        assert call_kwargs["parameters"]["workers"]["slug"] == test_result_worker_type
        assert call_kwargs["parameters"]["workers"]["replicas"] == test_result_worker_replicas
        assert call_kwargs["parameters"]["parameter_servers"]["slug"] == test_result_ps_type
        assert call_kwargs["parameters"]["parameter_servers"]["replicas"] == test_result_ps_replicas

    @pytest.mark.parametrize(
        "ps_replicas, worker_replicas, expected_warning_set",
        [
            (2, 2, set()),
            (5, 10, set()),
            (6, 8, {"Caution: You are creating a job with more than 5 parameter servers."}),
            (3, 12, {"Caution: You are creating a job with more than 10 workers."}),
            (18, 12, {"Caution: You are creating a job with more than 10 workers.",
                      "Caution: You are creating a job with more than 5 parameter servers."}),
        ])
    def test_when_warning_condition_is_not_met_then_warning_is_not_added_to_internal_warning_list(self,
                                                                                                  client_create_job,
                                                                                                  kwargs,
                                                                                                  ps_replicas,
                                                                                                  worker_replicas,
                                                                                                  expected_warning_set):
        assert clusterone.business_logic.job_commands.PS_REPLICAS_WARNING_THRESHOLD == 5
        assert clusterone.business_logic.job_commands.WORKER_REPLICAS_WARNING_THRESHOLD == 10
        kwargs["ps_replicas"] = ps_replicas
        kwargs["worker_replicas"] = worker_replicas
        command = CreateDistributedJobCommand(client=client_create_job, kwargs=kwargs)

        result = command.execute()

        assert result["warnings"] == expected_warning_set


class TestCreateSingleJobCommand(object):
    def test_mode_is_single(self, client_create_job, kwargs):
        """
        Mode should be single and workers replicas should be 1
        """

        command = CreateSingleJobCommand(client=client_create_job, kwargs=kwargs)
        command.execute()

        _, call_kwargs = client_create_job.create_job.call_args

        assert call_kwargs["parameters"]["mode"] == "single"
        assert call_kwargs["parameters"]["workers"]["replicas"] == 1

    @pytest.mark.parametrize("test_input,expected_result", [
        ("test_machine_slug",) * 2,
        ("other_machine_slug",) * 2,
    ])
    def test_when_instance_type_is_passed_then_is_present_in_api_call(self, client_create_job, kwargs, test_input,
                                                                      expected_result):
        """
        Given an instance type in the kwargs it should be reflected in the job configuration
        """

        kwargs["instance_type"] = test_input

        command = CreateSingleJobCommand(client=client_create_job, kwargs=kwargs)
        command.execute()

        _, call_kwargs = client_create_job.create_job.call_args

        assert call_kwargs["parameters"]["workers"]["slug"] == expected_result

    def test_returns_output_relative_job_path(self, client_create_job, kwargs):
        command = CreateSingleJobCommand(client=client_create_job, kwargs=kwargs)
        command_result = command.execute()

        assert command_result["output"] == "sample_project/sample_job"


class TestStartJobCommand(object):

    def test_when_command_is_executed_then_client_call_is_made(self, client_start_job):
        command = StartJobCommand(client=client_start_job, job_identifier="sample/job/path")
        command.execute()

        client_start_job.start_job.assert_called_with(job_identifier="sample/job/path")

    @pytest.mark.parametrize("test_path, test_current_user_username, expected_result",
                             [
                                 ("user/project/job", "user", "project/job"),
                                 ("user/project/job", "not_user", "user/project/job"),
                                 ("user/project/job", "definitely_not_user", "user/project/job"),
                             ])
    def test_when_command_is_executed_returns_job_path_in_the_output(self, client_start_job, test_path,
                                                                     test_current_user_username, expected_result):
        client_start_job.start_job.return_value.update({"path": test_path})
        client_start_job.username = test_current_user_username
        command = StartJobCommand(client=client_start_job, job_identifier="sample/job/path")

        result = command.execute()

        assert result["output"] == expected_result


class TestRunJobCommand(object):
    @pytest.mark.parametrize("start_warnings, create_warnings, expected_warnings", [
        (set(), set(), set()),
        ({"a"}, set(), {"a"}),
        (set(), {"b"}, {"b"}),
        ({"a", "c"}, {"b", "d"}, {"a", "b", "c", "d"}),
    ])
    def test_when_command_is_executed_returns_warnings_of_subcommands(self, start_warnings, create_warnings,
                                                                      expected_warnings, mocker):
        start_job_command_cls_mock = mocker.Mock(spec=StartJobCommand)
        start_job_command_mock = mocker.Mock(spec=StartJobCommand)

        start_job_command_cls_mock.return_value = start_job_command_mock
        start_job_command_mock.execute.return_value = {
            "warnings": start_warnings,
            "data": {"id": "some id"},
            "output": "some output",
        }

        # Single and Distributed implement the same interface
        create_job_command_cls_mock = mocker.Mock(spec=CreateSingleJobCommand)
        create_job_command_mock = mocker.Mock(spec=CreateSingleJobCommand)

        create_job_command_cls_mock.return_value = create_job_command_mock
        create_job_command_mock.execute.return_value = {
            "warnings": create_warnings,
            "data": {"id": "some id"},
            "output": "some output",
        }

        class MyRunJobCommand(RunJobCommand):
            create_job_command_cls = create_job_command_cls_mock

        command = MyRunJobCommand(start_job_command_cls=start_job_command_cls_mock)
        result = command.execute()

        assert result["warnings"] == expected_warnings
