import os

import click
from click import Choice, Path
from click import IntRange

from clusterone import run_tf

try:
    from math import inf
except ImportError as exception:
    inf = float('inf')

# TODO: Move this to utilities
POSITIVE_INTEGER = IntRange(1, inf)


def validate_mode(ctx, param, value):
    return "single-node" if value == "single" else value


def validate_env(ctx, param, value):
    return False if value == "new" else True


@click.command()
@click.pass_context
@click.argument(
    "mode",
    type=Choice(["single", "distributed"]),
    callback=validate_mode,
)
@click.option(
    "--command",
    type=Path(),
    default="python -m main",
    help="Command to run. Default: \"python -m main\"",
)
@click.option(
    "--worker-replicas",
    type=POSITIVE_INTEGER,
    default=2,
    help="Number of worker instances. Default: 2",
)
@click.option(
    "--ps-replicas",
    type=POSITIVE_INTEGER,
    default=1,
    help="Number of parameter server instances. Default: 1",
)
@click.option(
    "--requirements",
    type=Path(exists=True),
    default="./requirements.txt",
    help="Requirements file to use. Default: requirements.txt",
)
@click.option(
    "--env",
    type=Choice(["current", "new"]),
    default="new",
    callback=validate_env,
    help="Environment to run the job in - 'new' rebuilds the environment from scratch"
         ", 'current' reuses the current environment. Default: new",
)
def command(context, mode, command, env, requirements, worker_replicas, ps_replicas):
    """
    Run job locally on a simulated server environment.

    MODE < single | distributed >
    """

    run_tf(
        cwd=os.getcwd(),
        command=command,
        mode=mode,
        worker_replicas=worker_replicas,
        ps_replicas=ps_replicas,
        requirements=requirements,
        current_env=env
    )
