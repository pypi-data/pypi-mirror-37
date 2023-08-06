from django.apps import AppConfig


class DjflocashConfig(AppConfig):
    name = 'djflocash'
    verbose_name = "Django flocash"

    def ready(self):
        from . import signals  # noqa
