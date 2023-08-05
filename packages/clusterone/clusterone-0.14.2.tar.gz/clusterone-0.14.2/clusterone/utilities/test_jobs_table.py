from clusterone.utilities.jobs_table import _prepare_table_row, prepare_jobs_table_rows


class TestJobsTable:
    FAKE_JOBS_LIST = ['job1', 'job2', 'job3']

    def test_should_return_an_iterable_with_job_data_when_valid_job_dict_was_passed(self):
        job = {
            'owner': 'keton',
            'display_name': 'keton_name',
            'job_id': 'keton_id',
            'repository_owner': 'keton_owner',
            'repository_name': 'keton_repo_name',
            'git_commit_hash': 'keton_hash',
            'status': 'keton_status',
            'launched_at': 'keton_time',
        }

        row = _prepare_table_row(1, job)

        assert row == (1, 'keton/keton_name', 'keton_id', 'keton_owner/keton_repo_name:keton_ha',
                       'keton_status', 'keton')

    def test_should_return_table_string_when_jobs_iterable_provided(self, mocker):
        make_table_mock = mocker.MagicMock()
        make_table_mock.return_value = 'fake_table'
        _prepare_table_row_mock = mocker.MagicMock()
        _prepare_table_row_mock.return_value = 'fake_table_row'

        table = prepare_jobs_table_rows(self.FAKE_JOBS_LIST, make_table_func=make_table_mock,
                                        prepare_table_row=_prepare_table_row_mock)

        _prepare_table_row_mock.assert_has_calls([mocker.call(1, 'job1'), mocker.call(2, 'job2'), mocker.call(3, 'job3')])
        make_table_mock.assert_called_once_with(['fake_table_row', 'fake_table_row', 'fake_table_row'],
                                                ['#', 'Name', 'Id', 'Project', 'Status', 'Launched at'])
        assert table == 'fake_table'
