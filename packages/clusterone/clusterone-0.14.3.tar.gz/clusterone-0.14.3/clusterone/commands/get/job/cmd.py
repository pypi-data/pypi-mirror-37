import click

from clusterone import authenticate
from clusterone.utilities import make_table, serialize_job

HEADER = ['Property', 'Value']

HEADER_BASE = [
    'Name',
    'Status',
    'Project',
    'Command',
    #'Datasets',
    'Python version',
    'Package manager',
    'Requirements',
    'Framework',
    'Framework version',
    'Mode',
    'Worker type',
    'Worker replicas',
    'Ps type',
    'Ps replicas',
    'Time limit',
    ]

#TODO: Test this thoughrilly in the future -> [], [dataset], [dataset] * 3
def displayable_data(datasets_list):
    return "".join(["{}:{}\n".format(dataset['mount_point'], dataset['hash']) for dataset in datasets_list])

def extract_data_from_job(job):

    mode = job['parameters']['mode']

    excluded_fields = \
        ["Ps type", "Worker replicas", "Ps replicas"] if mode == "single" \
        else []

    extracted_data = [
        job['display_name'],
        job['status'],
        job['repository_name'],
        job['parameters']['command'],
        #displayable_data(job['parameters']['datasets']),
        job['parameters']['package_manager'],
        job['parameters']['requirements'],
        job['parameters']['framework']['name'],
        job['parameters']['framework']['version'],
        mode,
        job['parameters']['workers']['type'],
        job['parameters']['workers']['replicas'],
        job['parameters'].get('parameter_servers', {}).get('type'),
        job['parameters'].get('parameter_servers', {}).get('replicas'),
        "{} minutes".format(job['parameters']['time_limit']),
    ]

    job_data = []
    for header, value in zip(HEADER_BASE, extracted_data):
        if header not in excluded_fields:
            job_data.append((header, value))

    return job_data


@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'job-path-or-id',
    )
def command(context, job_path_or_id):
    """
    Get information about a job
    """

    job = serialize_job(job_path_or_id, context=context)

    click.echo(make_table(extract_data_from_job(job), header=HEADER))

    return job
