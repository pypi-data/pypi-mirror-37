import click
from click import echo

from clusterone import authenticate
from clusterone import client
from clusterone.just_types import Notebook


@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'notebook',
    type=Notebook(),
)
def command(context, notebook):
    """
    Stops and takes a snapshot of an existing notebook

    NOTEBOOK: path or uuid of an existing notebook
    """

    click.secho("Notebooks are in alpha, unexpected behavior is expected.", fg="yellow")

    notebook.stop(client)
    echo(notebook.id)
