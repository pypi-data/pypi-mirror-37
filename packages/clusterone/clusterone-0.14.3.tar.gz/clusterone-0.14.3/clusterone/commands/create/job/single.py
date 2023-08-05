import click

from clusterone import client
from clusterone.business_logic.job_commands import CreateSingleJobCommand
from clusterone.utilities import Choice
from .base_cmd import job_base_options


@job_base_options()
@click.pass_obj
@click.option(
    '--instance-type',
    type=Choice(client.instance_types_slugs),
    default="t2.small",
    help="Type of instance")
def command(context, **kwargs):
    """
    Creates a single-node job.
    """

    cmd = CreateSingleJobCommand(client=context.client, kwargs=kwargs)

    result = cmd.execute()

    click.echo(result["output"])
