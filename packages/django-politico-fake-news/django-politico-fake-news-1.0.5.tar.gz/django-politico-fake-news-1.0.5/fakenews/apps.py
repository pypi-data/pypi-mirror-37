from django.apps import AppConfig


class FakenewsConfig(AppConfig):
    name = 'fakenews'

    def ready(self):
        from fakenews import signals  # noqa
