from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from .mixins import DragonViewMixin
from .forms import *
from .utils import *


class DragonSearchAdminView(DragonViewMixin, FormView):
    template_name = "dragon/search.html"
    form_class = SearchForm
    page_title = "Search"

    def form_valid(self, form):
        data = form.cleaned_data

        cache = CacheManager(data["cache"])

        keys = cache.search(data["query"].split(","))

        if not len(keys):
            messages.add_message(
                self.request,
                messages.WARNING,
                f"No keys returned for query in cache. Cache: {data['cache']} - Query: {data['query']}"
            )
            return HttpResponseRedirect(reverse('dragon_search'))

        return HttpResponseRedirect(f"{reverse('dragon_results')}?c={data['cache']}&k={','.join(keys)}")


class DragonResultsAdminView(DragonViewMixin, TemplateView):
    template_name = "dragon/results.html"
    page_title = "Search Results"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cache = CacheManager(self.request.GET.get("c"))
        self.keys = self.request.GET.get("k").split(",")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['keys'] = self.keys
        ctx['cache'] = self.cache.display

        return ctx
    
    def post(self, *args, **kwargs):
        keys = self.request.POST.getlist('key')

        self.cache.cache.delete_many(keys)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Successfully deleted {len(keys)} keys from cache. Cache: {self.cache.display} - Keys: {', '.join(keys)}"
        )

        return HttpResponseRedirect(reverse('dragon_search'))


class DragonRedisKeyIndexAdminView(DragonViewMixin, TemplateView):
    template_name = "dragon/redis_key_index.html"
    page_title = "Redis Cache Index"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["redis_keys"] = {}

        for cache_name in settings.CACHES.keys():
            cache = CacheManager(cache_name)

            if not cache.is_redis:
                continue

            ctx["redis_keys"][cache_name] = cache.cache.keys("*")

        return ctx
