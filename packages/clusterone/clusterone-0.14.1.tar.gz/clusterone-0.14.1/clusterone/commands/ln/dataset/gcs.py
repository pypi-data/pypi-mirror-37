import click

from clusterone import authenticate
from clusterone.business_logic.dataset_commands import LinkGCSDatasetCommand


@click.command()
@click.pass_obj
@click.argument('bucket_identifier', nargs=1)
@click.option(
    '--name',
    '-n',
    help="Custom dataset name",
    required=False
)
@authenticate()
def command(context, bucket_identifier, name):
    link_command = LinkGCSDatasetCommand(context.client, bucket_identifier, name)
    result = link_command.execute()

    if result['errors']:
        click.echo(result['errors'])

    click.echo(result['output'])
