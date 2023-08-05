import raven
from click import echo


def log_click_error(message):
    echo("Error: {}".format(message), err=True)


class UncaughtExceptionHandler(object):
    """
    Passes unhandled exception to remote exception handler

    For local development in that case the exceptions should be printed to stdout
    """

    DEFAULT_SERVER_NAME = 'Clusterone CLI'

    def __init__(self, enable_sentry=None, sentry_dsn=None, release=None):
        self.enable_sentry = enable_sentry
        self.sentry_dsn = sentry_dsn
        self.release = release
        self.raven = None

        if self.enable_sentry:
            self.raven = raven.Client(dsn=self.sentry_dsn, release=self.release, name=self.DEFAULT_SERVER_NAME)

    def handle_exception(self, exception):
        if self.enable_sentry:
            self.raven.captureException()
        else:
            raise exception
