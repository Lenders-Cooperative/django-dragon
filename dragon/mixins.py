from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from .utils import has_redis_cache


__all__ = [
    "DragonViewMixin",
]


class DragonViewMixin(UserPassesTestMixin):
    page_title = None

    def test_func(self):
        if settings.DRAGON_USER_TEST_CALLBACK:
            return settings.DRAGON_USER_TEST_CALLBACK(self.request)
        
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = 'Dragon'

        if self.page_title:
            ctx['page_title'] = self.page_title

        ctx['has_redis_cache'] = has_redis_cache()

        return ctx
