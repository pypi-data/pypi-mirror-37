import re as regexp
from collections import OrderedDict
from functools import reduce

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

import click
from click.exceptions import BadParameter

from clusterone import client, authenticate
from clusterone.utilities import random_job_name, path_to_project, time_limit_to_minutes, path_to_dataset, Choice


def validate_name(context, parameters, value):
    if not regexp.match("^[a-zA-Z0-9_-]+$", value):
        raise BadParameter("Should only contain alphanumeric characters, \"_\", or \"-\".")

    return value


def validate_time_limit(context, parameters, value):
    try:
        return time_limit_to_minutes(value)
    except ValueError:
        raise BadParameter("Please conform to [hours]h[minutes]m format, e.g. \"20h12m\".")


def combine_options(options):
    """
    Generates a single decorator out of list of options decorator
    """

    def wrapper(function):
        return reduce(lambda decoratee, option_decorator: option_decorator(decoratee), reversed(options), function)

    return wrapper


def job_base_options(project_required=True):
    """
    Provides customization on the base
    """

    _job_base_options = [
        # This is used to process user defined arguments
        # See to learn more: http://click.pocoo.org/6/advanced/#forwarding-unknown-options
        click.command(context_settings=dict(
            ignore_unknown_options=True,
        )),

        # Common options for implementation
        authenticate(),

        # Business logic common options
        click.option(
            '--name',
            default=random_job_name(),
            callback=validate_name,
            help='Name of the job to be created',
        ),
        click.option(
            '--commit',
            help="Hash of commit to be run. Default: latest",
        ),
        click.option(
            '--datasets',
            help="Comma-separated list of the datasets to use for the job. Format: \"username/dataset-name\", e.g. 'clusterone/mnist-training:[GIT COMMIT HASH],clusterone/mnist-val:[GIT COMMIT HASH]'",
            default="",
        ),
        click.option(
            '--command',
            default='python -m main',
            help='The container entrypoint. Default: \"python -m main"',
        ),
        click.option(
            '--docker-image',
            type=Choice(client.framework_slugs),
            help='Docker image to be used.',
        ),
        click.option(
            '--package-manager',
            type=Choice(['pip', 'conda', 'anaconda']),
            default="pip",
            help='Package manager to use. Default: pip',
        ),
        click.option(
            '--requirements',
            help="Requirements file to use. Default: requirements.txt",
        ),
        # TODO: Create custom click type time
        # https://github.com/click-contrib/click-datetime ?
        click.option(
            '--time-limit',
            default="48h",
            callback=validate_time_limit,
            help="Time limit for the job. Format: [hours]h[minutes]m, e.g. \"22h30m\""
        ),
        click.option(
            '--description',
            default="",
            help='Job description'
        ),
        click.option(
            '--gpu-count',
            type=click.IntRange(0, float('inf')),
            help="Number of instance GPUs to be used. Defaults to max instance's GPU count",
        ),
    ]

    project_option = click.option(
        '--project',
        'project_path',
        required=project_required,
        help="Project path to be run. Format: \"username/project-name\"",
    )

    return combine_options(_job_base_options + [project_option])


def _prepare_list_of_datasets(context, kwargs):
    if not kwargs['datasets']:
        return []

    datasets_list = []
    for raw_dataset_string in kwargs['datasets'].split(','):
        dataset_dict = OrderedDict()
        try:
            raw_dataset_string = raw_dataset_string.strip()
            dataset_path, dataset_commit = raw_dataset_string.split(':')
        except ValueError:
            dataset_path = raw_dataset_string
        else:  # no exception raised
            if dataset_commit:
                dataset_dict['git_commit_hash'] = dataset_commit

        dataset = path_to_dataset(dataset_path, context=context)
        dataset_dict['dataset'] = dataset['id']
        datasets_list.append(dataset_dict)

    return datasets_list


def base(context, kwargs):
    """
    Common option processing login for all job types
    """
    if kwargs['project_path']:
        project = path_to_project(kwargs['project_path'], context=context)
        project_id = project['id']
    else:
        project_id = None

    datasets_list = _prepare_list_of_datasets(context, kwargs)

    framework_slug = kwargs['docker_image']

    package_manager = kwargs['package_manager']
    package_manager = 'conda' if package_manager == 'anaconda' else package_manager

    requirements = kwargs['requirements']
    default_requirements = "requirements.{}".format("txt" if package_manager == 'pip' else "yml")
    requirements = default_requirements if not requirements else requirements

    context = {
        'parameters':
            {
                "command": kwargs['command'],
                "package_manager": package_manager,
                "requirements": requirements,
                "time_limit": kwargs['time_limit'],
                "repository": project_id,
                "framework":
                    {
                        "slug": framework_slug
                    },
                "datasets_set": datasets_list,
                "workers": {},
            },
        'meta':
            {
                "name": kwargs['name'],
                "description": kwargs['description'],
            }
    }

    gpu_count = kwargs.get('gpu_count')
    if gpu_count is not None:
        context['parameters']['workers']['gpu'] = gpu_count

    commit = kwargs['commit']
    if commit:
        context['parameters']['git_commit_hash'] = commit

    return context
