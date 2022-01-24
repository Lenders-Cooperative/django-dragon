from django.urls import path
from .views import *


urlpatterns = [
    path(
        '',
        DragonSearchAdminView.as_view(),
        name="dragon_search"
    ),
    path(
        'results',
        DragonResultsAdminView.as_view(),
        name="dragon_results"
    ),
    path(
        'redis-index',
        DragonRedisKeyIndexAdminView.as_view(),
        name="dragon_redis_index"
    ),
]
