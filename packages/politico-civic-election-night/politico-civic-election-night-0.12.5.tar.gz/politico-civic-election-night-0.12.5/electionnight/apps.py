from django.apps import AppConfig


class ElectionnightConfig(AppConfig):
    name = "electionnight"

    def ready(self):
        from electionnight import signals
