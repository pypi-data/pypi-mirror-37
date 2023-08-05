import click

from clusterone import client
from clusterone.business_logic.job_commands import RunSingleJobCommand
from clusterone.utilities import Choice
from clusterone.commands.create.job.base_cmd import job_base_options


@job_base_options()
@click.pass_obj
@click.option(
    '--instance-type',
    type=Choice(client.instance_types_slugs),
    default="t2.small",
    help="Type of instance")
def command(context, **kwargs):
    """
    Create and start a single-node job.
    """

    cmd = RunSingleJobCommand(client=context.client, kwargs=kwargs)

    result = cmd.execute()

    for warning in result["warnings"]:
        click.echo(warning)

    click.echo(result["output"])

