import click

from clusterone import authenticate
from clusterone.business_logic.job_commands import StartJobCommand


@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'job_identifier',
)
def command(context, job_identifier):
    """
    Runs an existing job, identified either by name or ID
    """

    cmd = StartJobCommand(client=context.client, job_identifier=job_identifier)

    result = cmd.execute()

    click.echo(result["output"])
