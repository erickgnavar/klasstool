from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'klasstool.polls'

    def ready(self):
        from . import signals  # noqa
