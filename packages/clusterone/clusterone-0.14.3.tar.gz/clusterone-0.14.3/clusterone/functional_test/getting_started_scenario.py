from contextlib import suppress
from os import getenv
from datetime import datetime

from clusterone import ClusteroneClient
from .actions import register_user, login, init_gitlab_project_from_clusterone_samples, start_job, create_job, set_endpoint, logout, \
    check_outputs
from .scenario import Scenario
from .types import Output, UserCredentials
from .utilities import generate_random_credentials, authorize_client_via_session_file, poll


class GettingStarted(Scenario):
    """
    Mimicking programmatically our onboarding tutorial
    """

    def __init__(self):
        testuser_password = getenv('PASSWORD')
        testuser_email = getenv('EMAIL')
        testuser_username = getenv('USERNAME')

        now = datetime.now()

        self.url = "https://clusterone.com/api/"

        # to ensure project uniqueness while running different tests on the same user
        project_salt = generate_project_salt(time=now)
        self.project_name = "clusterone-test-onboarding-{}".format(project_salt)

        self.project_url = "https://github.com/clusterone/self-driving-demo"

        self.job_name = "clusterone-test-job"
        self.testing_credentials = UserCredentials(
            username=testuser_username,
            password=testuser_password,
            email=testuser_email,
        )

        self.any_output_timeout = 600  # seconds
        self.checkpoint_output_timeout = 600  # seconds
        self.loss_output_timeout = 600  # seconds
        self.poll_interval = 10  # seconds

        self.client = ClusteroneClient(username=self.testing_credentials.username, api_url=self.url)

        logout()
        set_endpoint(self.url)

    def run(self):
        login(self.testing_credentials)

        # This is a hax
        authorize_client_via_session_file(client=self.client)

        init_gitlab_project_from_clusterone_samples(name=self.project_name, project_url=self.project_url)

        create_job(self.project_name, self.job_name, command="python -m main_tf", framework="tensorflow-1.3.0", dataset="tensorbot/self-driving-demo-data")
        start_job(self.project_name, self.job_name)

        # TODO: Test for events to know when the pods have started
        # TODO: After that reduce the timeout on any outputs

        poll(check_outputs, args=(Output.ANY, self.job_name), kwargs={"client": self.client}, timeout=self.any_output_timeout,
            interval=self.poll_interval)

        poll(check_outputs, args=(Output.CHECKPOINT, self.job_name), kwargs={"client": self.client},
             timeout=self.checkpoint_output_timeout,
             interval=self.poll_interval)

        poll(check_outputs, args=(Output.LOSS, self.job_name), kwargs={"client": self.client},
             timeout=self.loss_output_timeout,
             interval=self.poll_interval)

    def clean(self):
        # TODO: Do this better
        from .utilities import just_exec, call

        with suppress(AssertionError):
            # TODO: move this to actions
            just_exec("stop job -p {}/{}".format(self.project_name, self.job_name))

        # TODO: move this to actions
        call("rm -rf self-driving-demo", asserted=False)


def generate_project_salt(time):
    string_timestamp = str(time.timestamp())
    slug_friendly_salt = string_timestamp.replace('.', '-')

    return slug_friendly_salt
