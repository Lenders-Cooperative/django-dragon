# Django Dragon Cache Manager 🐲

A cache manager for Django admin.

```
"What did he promise you, a share of the treasure? As if it was his to give.
I will not part with a single coin! Not one piece of it!"

- Smaug
```

## Installation

1. Install the package: `pip install django-dragon`
2. Add `dragon_cache_manager` to your `INSTALLED_APPS` in Django settings.
3. Add the Dragon URLs **before** `admin/`: `path('admin/dragon/', include('dragon_cache_manager.urls')),`
4. Dragon will be accessible from `/admin/dragon`.

## Configuration

All Dragon settings are prefixed by `DRAGON_`. 

### `USER_TEST_CALLBACK`

`request` is the only argument and is the current `Request` instance.

Callback for determining access to the Dragon pages.

Should return `True` if allowed. Otherwise, `False`.

By default, any staff or superuser will be able to access Dragon.

### `USER_IS_SUPERUSER`

Indicates if a superuser is allowed to view Dragon.

Default: `True`

### `USER_IS_STAFF`

Same as `USER_IS_SUPERUSER` but for staff. 

Default: `False`

### `ENABLE_INDEX`

Indicates if the Redis key index should be shown.

Default: `False`

### `MAX_RESULTS`

Maximum number of results to return on a key search.

Default: `50`

## Commands

### `load_test_cache`

Adds X keys to a cache specified in `settings.CACHES`. 

For each key, a random word from `dragon/management/commands/random_words.txt` will be used as the key and value.

- `-c/--cache` - Specify the name of the cache to populate (defaults to all).
- `-k/--keys` - Specify the number items to generate (defaults to 50).
