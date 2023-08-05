from clusterone.utilities import make_table

TABLE_HEADERS = ['#', 'Name', 'Id', 'Project', 'Status', 'Launched at']


def _prepare_table_row(i, job):
    name = '%s/%s' % (job.get('owner'), job.get('display_name'))
    id_ = job['job_id']
    project = '%s/%s:%s' % (job.get('repository_owner'), job.get('repository_name'), job['git_commit_hash'][:8])
    status = job.get('status')
    launched_at = '' if job.get('launched_at') is None else job.get('launched_at')[:-5]

    return i, name, id_, project, status, launched_at


def prepare_jobs_table_rows(jobs, make_table_func=make_table, prepare_table_row=_prepare_table_row):
    table_data = []
    for i, job in enumerate(jobs, 1):
        row = prepare_table_row(i, job)
        table_data.append(row)

    table = make_table_func(table_data, TABLE_HEADERS)
    return table
