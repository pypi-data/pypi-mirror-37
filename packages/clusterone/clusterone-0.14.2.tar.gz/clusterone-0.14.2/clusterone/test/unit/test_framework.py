"""
This file as of now contains only test for job creation - if it expands consider splitting
"""

import pytest
from click.testing import CliRunner

from clusterone.business_logic.job_commands import CreateSingleJobCommand, CreateDistributedJobCommand, \
    RunSingleJobCommand, RunDistributedJobCommand
from clusterone.business_logic.notebook_commands import ListNotebooksCommand
from clusterone.client_exceptions import InvalidParameter
from clusterone.clusterone_cli import cli


class TestJustCreateJobSingle(object):
    @pytest.fixture
    def command_mock(self, mocker):
        cmd_mock = mocker.Mock(spec=CreateSingleJobCommand)
        cmd_mock.execute.return_value = {"display_name": "sample_job", "repository_name": "sample_project",
                                         "job_id": "some_uuid"}

        mocker.patch("clusterone.commands.create.job.single.CreateSingleJobCommand", return_value=cmd_mock)

        return cmd_mock

    def test_when_executed_outputs_command_result_output(self, command_mock):

        command_mock.execute.return_value = {"output": "sample command output"}

        result = CliRunner().invoke(cli, [
            "create",
            "job",
            "single",
            "--project", "sample_project",
        ])

        assert result.output == "sample command output\n"


class TestJustCreateJobDistributed(object):

    @pytest.fixture
    def threshold_mocks(self, mocker):
        mocker.patch("clusterone.commands.create.job.distributed.PS_REPLICAS_WARNING_THRESHOLD", new=6)
        mocker.patch("clusterone.commands.create.job.distributed.WORKER_REPLICAS_WARNING_THRESHOLD", new=11)

    @pytest.fixture
    def command_mock(self, mocker):
        cmd_mock = mocker.Mock(spec=CreateDistributedJobCommand)
        cmd_mock.execute.return_value = {"display_name": "sample_job", "repository_name": "sample_project",
                                         "job_id": "some_uuid"}

        mocker.patch("clusterone.commands.create.job.distributed.CreateDistributedJobCommand", return_value=cmd_mock)

        return cmd_mock

    @pytest.mark.parametrize("warnings_array, expected_output", [
        (["warning one", "warning two", "warning three"], "warning one\nwarning two\nwarning three\nsample command output\n"),
        (["warning one"], "warning one\nsample command output\n"),
        ([], "sample command output\n"),
    ])
    def test_when_executed_outputs_command_warnings_and_output(self, command_mock, warnings_array, expected_output):
        command_mock.execute.return_value = {"warnings": warnings_array, "output": "sample command output"}

        result = CliRunner().invoke(cli, [
            "create",
            "job",
            "distributed",
            "--project", "sample_project",
        ])

        assert result.output == expected_output

    def test_exception_re_raise(self, command_mock):
        command_exception = InvalidParameter("something went wrong", parameter="framework")
        command_mock.execute.side_effect = command_exception

        result = CliRunner().invoke(cli, [
            "create",
            "job",
            "distributed",
            "--project", "sample_project",

        ])

        assert result.exit_code == 2
        assert "Error: Invalid value for --framework: something went wrong" in result.output


class TestJustStartJob(object):
    @pytest.fixture()
    def command_mock(self, mocker):
        mock = mocker.Mock(spec=CreateDistributedJobCommand)
        mock.execute.return_value = {"output": "sample command output"}

        mocker.patch("clusterone.commands.start.job.cmd.StartJobCommand", return_value=mock)

        return mock

    def test_when_executed_outputs_command_result_output(self, command_mock):
        result = CliRunner().invoke(cli, [
            "start",
            "job", "project/job",
        ])

        assert result.output == "sample command output\n"


class TestJustRunSingleJob(object):
    @pytest.fixture()
    def command_mock(self, mocker):
        mock = mocker.Mock(spec=RunSingleJobCommand)

        mocker.patch("clusterone.commands.run.job.single.RunSingleJobCommand", return_value=mock)

        return mock

    @pytest.mark.parametrize("warnings_set, expected_output", [
        (set(), "sample command output\n"),
    ])
    def test_when_executed_outputs_command_warnings_and_output(self, command_mock, warnings_set, expected_output):
        command_mock.execute.return_value = {"warnings": warnings_set, "output": "sample command output"}

        result = CliRunner().invoke(cli, [
            "run",
            "job",
            "single",
            "--project", "sample_project",
        ])

        assert result.output == expected_output


class TestJustRunDistributedJob(object):
    @pytest.fixture()
    def command_mock(self, mocker):
        mock = mocker.Mock(spec=RunDistributedJobCommand)

        mocker.patch("clusterone.commands.run.job.distributed.RunDistributedJobCommand", return_value=mock)

        return mock

    @pytest.mark.parametrize("warnings_set, expected_outputs", [
        ({"warning one", "warning two", "warning three"},
         {"warning one", "warning two", "warning three", "sample command output"}),
        ({"warning one"}, {"warning one", "sample command output"}),
        (set(), {"sample command output"}),
    ])
    def test_when_executed_outputs_command_warnings_and_output(self, command_mock, warnings_set, expected_outputs):
        command_mock.execute.return_value = {"warnings": warnings_set, "output": "sample command output"}

        result = CliRunner().invoke(cli, [
            "run",
            "job",
            "distributed",
            "--project", "sample_project",
        ])

        assert all(string in result.output for string in expected_outputs)

    def test_exception_re_raise(self, command_mock):
        command_exception = InvalidParameter("something went wrong", parameter="framework")
        command_mock.execute.side_effect = command_exception

        result = CliRunner().invoke(cli, [
            "run",
            "job",
            "distributed",
            "--project", "sample_project",

        ])

        assert result.exit_code == 2
        assert "Error: Invalid value for --framework: something went wrong" in result.output


class TestJustGetNotebooks(object):
    @pytest.fixture()
    def command_mock(self, mocker):
        mock = mocker.Mock(spec=ListNotebooksCommand)

        mocker.patch("clusterone.commands.get.notebooks.cmd.ListNotebooksCommand", return_value=mock)

        return mock

    def test_when_executed_outputs_command_warnings_and_output(self, command_mock):
        command_mock.execute.return_value = {"output": "sample command output"}

        result = CliRunner().invoke(cli, [
            "get",
            "notebooks",
        ])

        assert "sample command output\n" in result.output

