from django.core.cache import (
    caches,
    InvalidCacheBackendError
)
from django.conf import settings


__all__ = [
    "get_caches", "has_redis_cache", "CacheManager",
]


def get_caches():
    caches = settings.CACHES or {}
    return [(key, f"{key} ({cache['BACKEND'].split('.').pop()})") for key, cache in caches.items()]


def has_redis_cache():
    return len([1 for name, backend in get_caches() if 'redis' in backend.lower()]) > 0


class CacheManager(object):
    def __init__(self, cache_name):
        self.cache = caches[cache_name]
        self.config = settings.CACHES[cache_name]
        self.name = cache_name
    
    @property
    def display(self):
        return dict(get_caches())[self.name]
    
    @property
    def is_redis(self):
        return 'redis' in self.config['BACKEND'].lower()
    
    def delete(self, key):
        self.cache.delete(key)
    
    def delete_many(self, keys):
        self.cache.delete_many(keys)
        
    def search(self, query, max_results=None):
        if not max_results:
            max_results = settings.DRAGON_MAX_RESULTS

        for term in query:
            if self.is_redis:
                results = []

                for key in self.cache.iter_keys(f"*{term}*"):
                    if len(results) == max_results:
                        break

                    results.append(key)

                return results
            else:
                return [term] if self.cache.get(term) is not None else []
