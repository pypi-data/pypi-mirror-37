import click

from clusterone import authenticate
from clusterone import client
from clusterone.utilities.jobs_table import prepare_jobs_table_rows


@click.command()
@click.pass_obj
@authenticate()
def command(context):
    """
    List jobs
    """
    _command(context)


def _command(context, api_client=client, prepare_row_func=prepare_jobs_table_rows, print_function=click.echo):
    """Actual command function. Made a separate function to be unit-testable"""
    jobs = api_client.get_jobs()
    if not jobs:
        print_function("You don't seem to have any jobs yet. Try just create a job to make one.")
        return

    table = prepare_row_func(jobs)
    print_function(table)
