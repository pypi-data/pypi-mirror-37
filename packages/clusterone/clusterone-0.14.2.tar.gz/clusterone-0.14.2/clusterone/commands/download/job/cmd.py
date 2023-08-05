# -*- coding: utf-8 -*-

import click
from clusterone import authenticate

from clusterone.business_logic.job_commands import DownloadJobCommand


@click.command()
@click.pass_obj
@authenticate()
@click.argument(
    'job_identifier'
)
@click.option(
    '--download_to',
    '-d',
    help='Path where to download')
def command(context, download_to, job_identifier):
    """
    Download all files related for the job
    """

    cmd = DownloadJobCommand(client=context.client, job_identifier=job_identifier, download_to=download_to)

    result = cmd.execute()

    for output in result:
        click.echo(output['data'])
