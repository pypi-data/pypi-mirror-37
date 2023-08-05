from clusterone.business_logic.command import Command
from clusterone.business_logic.generic_commands import ListCommand
from clusterone.just_client import Notebook


class CreateNotebookCommand(Command):
    JOB_MODE = 'single'
    WORKER_REPLICA_COUNT = 1
    JOB_FRAMEWORK = {'slug': 'jupyter'}

    def __init__(self, params, command_base, client, notebook_class=Notebook):
        self.context = params['context']
        self.kwargs = params['kwargs']
        self.command_base = command_base
        self.client = client
        self.notebook_class = notebook_class

    def execute(self):
        configuration = self._prepare_notebook_configuration()
        notebook = self.notebook_class(self.client, configuration)

        return notebook

    def _prepare_notebook_configuration(self):
        config = self.command_base(self.context, self.kwargs)
        notebook_configuration = config['parameters']
        notebook_meta = config['meta']

        notebook_configuration['mode'] = self.JOB_MODE
        notebook_configuration['workers'] = {'slug': self.kwargs['instance_type'],
                                             'replicas': self.WORKER_REPLICA_COUNT}
        notebook_configuration['framework'] = self.JOB_FRAMEWORK
        notebook_configuration.update(notebook_meta)

        return notebook_configuration


class ListNotebooksCommand(ListCommand):

    table_header = ("Name", "Id", "Project", "Status", "Latest snapshot")
    enumerate = True
    entity_name = "notebook"

    def _gather_entity_data(self):
        return self.client.get_notebooks()

    @staticmethod
    def _entity_to_row(entity_data):
        uuid = entity_data['job_id']
        status = entity_data["status"]
        notebook_path = entity_data["path"]  # this is displayed as "Name", yet technically it's a path
        latest_snapshot_identifier = entity_data["latest_snapshot_identifier"]

        project_owner = entity_data.get("repository_owner")
        project_name = entity_data.get("repository_name")
        commit_hash = entity_data.get("git_commit_hash")

        if project_owner and project_name and commit_hash:
            # first 7 digits were chosen to be consistent with behaviour of `git log --online`
            commit_path = "{project_owner}/{project_name}:{commit_hash:.7}".format(project_owner=project_owner,
                                                                                   project_name=project_name,
                                                                                   commit_hash=commit_hash)
        else:
            assert project_name is project_owner is commit_hash is None

            commit_path = "None"

        return notebook_path, uuid, commit_path, status, latest_snapshot_identifier
