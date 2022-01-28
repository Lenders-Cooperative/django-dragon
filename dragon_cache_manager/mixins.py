from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from .utils import *


__all__ = [
    "DragonViewMixin",
]


class DragonViewMixin(UserPassesTestMixin):
    page_title = None

    def test_func(self):
        if settings.DRAGON_USER_TEST_CALLBACK:
            return settings.DRAGON_USER_TEST_CALLBACK(self.request)

        if settings.DRAGON_USER_IS_SUPERUSER and self.request.user.is_superuser:
            return True

        if settings.DRAGON_USER_IS_STAFF and self.request.user.is_staff:
            return True

        return False
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = 'Cache Manager'

        if self.page_title:
            ctx['page_title'] = self.page_title

        ctx['has_redis_cache'] = has_redis_cache()
        ctx['show_redis_index'] = settings.DRAGON_ENABLE_INDEX

        return ctx
