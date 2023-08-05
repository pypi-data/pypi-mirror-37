import functools
import os
from abc import abstractmethod, ABCMeta

from clusterone.client_exceptions import InvalidParameter
from clusterone.utilities import deep_update
from clusterone.utilities import path_to_project, path_to_dataset
from .command import Command

PS_REPLICAS_WARNING_THRESHOLD = 5
WORKER_REPLICAS_WARNING_THRESHOLD = 10


def relative_job_path(absolute_job_path, current_user_username):
    """
    Strips current user information from job path.
    If the job belongs to someone else than the user information is left intact

    Examples:
        Given user USER and absolute job path USER/PROJECT/JOB
        relative_job_path(USER/PROJECT/JOB) == PROJECT/JOB

        Given user USER and absolute job path SOMEONE/PROJECT/JOB
        relative_job_path(SOMEONE/PROJECT/JOB) == SOMEONE/PROJECT/JOB.
    """

    if absolute_job_path.startswith(current_user_username):
        _relative_job_path = absolute_job_path.replace("{}/".format(current_user_username), "")
    else:
        _relative_job_path = absolute_job_path

    return _relative_job_path


class CreateJobCommand(Command):

    __metaclass__ = ABCMeta

    def __init__(self, client, kwargs=None):

        self.client = client
        self.kwargs = kwargs if kwargs is not None else {}
        self.job_configuration = {}

        self._warnings = set()
        self._data = {}

    @abstractmethod
    def _prepare_detailed_job_configuration(self):
        raise NotImplementedError()

    def _prepare_base_job_configuration(self):

        def _prepare_list_of_datasets(context, kwargs):
            if not kwargs['datasets']:
                return []

            datasets_list = []
            for raw_dataset_string in kwargs['datasets'].split(','):
                dataset_dict = {}
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

        class Context(object):
            def __init__(self, client, session, cwd):
                self.client = client
                self.session = session
                self.cwd = cwd

        context = Context(client=self.client, session={"username": self.client.username}, cwd="")

        if self.kwargs['project_path']:
            project = path_to_project(self.kwargs['project_path'], context=context)
            project_id = project['id']
        else:
            project_id = None

        datasets_list = _prepare_list_of_datasets(context, self.kwargs)

        framework_slug = self.kwargs['docker_image']

        package_manager = self.kwargs['package_manager']
        package_manager = 'conda' if package_manager == 'anaconda' else package_manager

        requirements = self.kwargs['requirements']
        default_requirements = "requirements.{}".format("txt" if package_manager == 'pip' else "yml")
        requirements = default_requirements if not requirements else requirements

        self.job_configuration = {
            'parameters':
                {
                    "command": self.kwargs['command'],
                    "package_manager": package_manager,
                    "requirements": requirements,
                    "time_limit": self.kwargs['time_limit'],
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
                    "name": self.kwargs['name'],
                    "description": self.kwargs['description'],
                }
        }

        gpu_count = self.kwargs.get('gpu_count')
        if gpu_count is not None:
            self.job_configuration['parameters']['workers']['gpu'] = gpu_count

        commit = self.kwargs['commit']
        if commit:
            self.job_configuration['parameters']['git_commit_hash'] = commit

    def execute(self):
        self._prepare_base_job_configuration()
        self._prepare_detailed_job_configuration()

        self._data = self.client.create_job(
            self.job_configuration['meta']['name'],
            description=self.job_configuration['meta']['description'],
            parameters=self.job_configuration['parameters'],
        )

        current_user_username = self.client.username
        # TODO: This is naive way of generating the job path and will fail for shared projects, need fix on API side
        # API should push the path to the consumers
        absolute_job_path = "{username}/{project}/{job_name}".format(username=current_user_username,
                                                                     project=self._data["repository_name"],
                                                                     job_name=self._data["display_name"])

        output = relative_job_path(absolute_job_path, current_user_username)

        return {
            "warnings": self._warnings,
            "data": self._data,
            "output": output,
        }


class CreateSingleJobCommand(CreateJobCommand):
    def _prepare_detailed_job_configuration(self):
        deep_update(self.job_configuration, {
            "parameters": {
                "mode": "single",
                "workers": {
                    "slug": self.kwargs["instance_type"],
                    "replicas": 1,
                },
            },
        })


class CreateDistributedJobCommand(CreateJobCommand):
    def execute(self):
        warning_template = "Caution: You are creating a job with more than {how_many} {of_what}s."

        if self.kwargs["ps_replicas"] > PS_REPLICAS_WARNING_THRESHOLD:
            self._warnings.add(warning_template.format(how_many=PS_REPLICAS_WARNING_THRESHOLD, of_what="parameter server"))

        if self.kwargs["worker_replicas"] > WORKER_REPLICAS_WARNING_THRESHOLD:
            self._warnings.add(warning_template.format(how_many=WORKER_REPLICAS_WARNING_THRESHOLD, of_what="worker"))

        return super(CreateDistributedJobCommand, self).execute()

    def _prepare_detailed_job_configuration(self):

        # TODO: Remove this once new SaSS version is deployed - also see distributed command
        if self.job_configuration['parameters']['framework']['slug'] == 'pytorch-1.0.0':
            raise InvalidParameter("PyTorch is only supported for single jobs.", parameter="framework")

        deep_update(self.job_configuration, {
            "parameters": {
                "mode": "distributed",
                "workers": {
                    "slug": self.kwargs["worker_type"],
                    "replicas": self.kwargs["worker_replicas"],
                },
                "parameter_servers": {
                    "slug": self.kwargs["ps_type"],
                    "replicas": self.kwargs["ps_replicas"],
                },
            },
        })


class StartJobCommand(Command):
    def __init__(self, client, job_identifier, *args, **kwargs):
        self.client = client
        self.job_identifier = job_identifier

        self._warnings = set()
        self._data = {}

    def execute(self):
        self._data = self.client.start_job(job_identifier=self.job_identifier)

        absolute_job_path = self._data["path"]
        current_user_username = self.client.username

        output = relative_job_path(absolute_job_path, current_user_username)

        return {
            "warnings": self._warnings,
            "data": self._data,
            "output": output,
        }


class RunJobCommand(Command):

    __metaclass__ = ABCMeta
    create_job_command_cls = None

    def __init__(self, start_job_command_cls=StartJobCommand, *args, **kwargs):
        self._create_command = self.create_job_command_cls(*args, **kwargs)
        self._partial_start_command = functools.partial(start_job_command_cls, *args, **kwargs)

        self._warnings = set()
        self._data = {}

    def execute(self):

        create_result = self._create_command.execute()

        start_command = self._partial_start_command(job_identifier=create_result["data"]["id"])
        start_result = start_command.execute()

        assert create_result["output"] == start_result["output"]

        return {
            "warnings": create_result["warnings"] | start_result["warnings"],
            "data": create_result["data"],  # start_result contains no unique data compared to create_result
            "output": start_result["output"],
        }


class RunSingleJobCommand(RunJobCommand):
    create_job_command_cls = CreateSingleJobCommand


class RunDistributedJobCommand(RunJobCommand):
    create_job_command_cls = CreateDistributedJobCommand


class DownloadJobCommand(Command):
    def __init__(self, client, job_identifier, download_to, *args, **kwargs):
        self.client = client
        self.job_identifier = job_identifier
        self.download_to = download_to

    def execute(self):

        warning_template = "Failed to download file {filename}, error: {error}"
        downloaded_template = 'Downloaded: {counter} | {name} | {size} kb'

        if not self.download_to:
            self.download_to = os.path.join(os.getcwd(), self.job_identifier)
            os.makedirs(self.download_to, exist_ok=True)

        if not os.path.isdir(self.download_to):
            raise OSError('Directory {} is not valid path'.format(self.download_to))

        list_of_files = self.client.get_file_list(self.job_identifier)
        counter = 0
        for file_to_download in list_of_files:
            # Display the files
            try:
                if file_to_download['size'] > 0:
                    # Save file in specified path
                    self.client.download_file(self.job_identifier, file_to_download['name'], path=os.path.join(self.download_to, file_to_download['name']))
                    counter += 1
                    downloaded_msg = downloaded_template.format(counter=counter, name=file_to_download['name'], size=file_to_download['size'] / 1024)

                    yield {
                            "data": downloaded_msg,
                            "output": 'Downloaded files: {}'.format(counter),
                    }

            except Exception as error:
                yield warning_template.format(filename=file_to_download['name'], error=error)
                continue
