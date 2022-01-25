from django.apps import AppConfig
from . import settings


class DragonCacheManagerConfig(AppConfig):
    name = 'dragon_cache_manager'

    def ready(self):
        settings.patch()
