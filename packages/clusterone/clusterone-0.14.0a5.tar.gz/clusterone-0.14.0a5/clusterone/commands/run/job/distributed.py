from clusterone.client_exceptions import InvalidParameter

try:
    from math import inf
except ImportError as exception:
    inf = float('inf')

import click
from click import IntRange, BadParameter

from clusterone import client
from clusterone.business_logic.job_commands import RunDistributedJobCommand
from clusterone.commands.create.job.base_cmd import job_base_options
from clusterone.utilities import Choice

# TODO: Move this to utilities
POSITIVE_INTEGER = IntRange(1, inf)


@job_base_options()
@click.pass_obj
@click.option(
    '--worker-type',
    type=Choice(client.instance_types_slugs),
    default="t2.small",
    help="Type of worker instances")
@click.option(
    '--ps-type',
    type=Choice(client.ps_type_slugs),
    default="t2.small",
    help="Type of parameter server instances")
@click.option(
    '--worker-replicas',
    type=POSITIVE_INTEGER,
    default=2,
    help="Number of worker instances",
)
@click.option(
    '--ps-replicas',
    type=POSITIVE_INTEGER,
    default=1,
    help="Number of parameter server instances",
)
def command(context, **kwargs):
    """
    Create and start a distributed job.
    """

    cmd = RunDistributedJobCommand(client=context.client, kwargs=kwargs)

    try:
        result = cmd.execute()
    except InvalidParameter as e:
        raise BadParameter(str(e), param_hint="--{}".format(e.parameter))

    for warning in result["warnings"]:
        click.echo(warning)

    click.echo(result["output"])

