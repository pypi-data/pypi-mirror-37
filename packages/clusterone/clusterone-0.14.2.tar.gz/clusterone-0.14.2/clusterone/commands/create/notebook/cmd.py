import click
from click import echo

from clusterone import client
from clusterone.business_logic.notebook_commands import CreateNotebookCommand
from clusterone.commands.create.job.base_cmd import job_base_options, base
from clusterone.utilities import Choice


@job_base_options(project_required=False)
@click.pass_obj
@click.option(
    '--instance-type',
    type=Choice(client.instance_types_slugs),
    default="t2.small",
    help="Type of single instance to run.")
def command(context, **kwargs):
    """
    Create a Jupyter notebook.
    """
    command_params = {'context': context,
                      'kwargs': kwargs}

    click.secho("Notebooks are in alpha, unexpected behavior is expected.", fg="yellow")

    create_notebook_command = CreateNotebookCommand(command_params, base, client)
    notebook = create_notebook_command.execute()

    echo('Notebook created. Run \033[32mjust start notebook {}/{}\033[0m to start it.'.format(notebook.owner,
                                                                                              notebook.name))
    echo('Notebook URL: {}/?token={}'.format(notebook.url, notebook.token))
