from clusterone.commands.get.jobs.cmd import _command


class TestGetJobsCommand:
    FAKE_JOB_OBJECTS_LIST = ['fake job1', 'fake job2']

    def test_should_print_error_message_when_no_jobs_were_found(self, mocker):
        api_client_mock = mocker.MagicMock()
        api_client_mock.get_jobs.return_value = []
        print_function_mock = mocker.MagicMock()

        _command({}, api_client=api_client_mock, print_function=print_function_mock)

        print_function_mock.assert_called_with("You don't seem to have any jobs yet. "
                                               "Try just create a job to make one.")

    def test_should_print_jobs_table_when_jobs_were_returned(self, mocker):
        api_client_mock = mocker.MagicMock()
        api_client_mock.get_jobs.return_value = self.FAKE_JOB_OBJECTS_LIST
        print_function_mock = mocker.MagicMock()
        prepare_row_func_mock = mocker.MagicMock()
        prepare_row_func_mock.return_value = 'fake table'

        _command({}, api_client=api_client_mock, prepare_row_func=prepare_row_func_mock,
                 print_function=print_function_mock)

        print_function_mock.assert_called_with('fake table')
        prepare_row_func_mock.assert_called_with(self.FAKE_JOB_OBJECTS_LIST)
