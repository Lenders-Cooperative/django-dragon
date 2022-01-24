from django.apps import AppConfig
from . import settings


class DragonConfig(AppConfig):
    name = 'dragon'

    def ready(self):
        settings.patch()