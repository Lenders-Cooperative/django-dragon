from django.conf import settings as dj_settings


__all__ = [
    "patch"
]


DEFAULT_SETTINGS = {
    "USER_TEST_CALLBACK": None,
    "USER_IS_SUPERUSER": True,
    "USER_IS_STAFF": False,
    "ENABLE_INDEX": False,
    "MAX_RESULTS": 50
}


def patch():
    for key, value in DEFAULT_SETTINGS.items():
        key = f"DRAGON_{key}"

        if not hasattr(dj_settings, key):
            setattr(dj_settings, key, value)
