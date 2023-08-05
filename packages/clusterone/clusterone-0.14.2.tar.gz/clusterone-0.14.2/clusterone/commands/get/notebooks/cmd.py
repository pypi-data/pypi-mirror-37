import click

from clusterone import authenticate
from clusterone.business_logic.notebook_commands import ListNotebooksCommand


@click.command()
@click.pass_obj
@authenticate()
def command(context):
    """
    List notebooks
    """

    click.secho("Notebooks are in alpha, unexpected behavior is expected.", fg="yellow")

    cmd = ListNotebooksCommand(client=context.client)
    result = cmd.execute()
    click.echo(result["output"])
