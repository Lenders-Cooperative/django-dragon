from django import forms
from .utils import *


__all__ = [
    'SearchForm',
]


def get_cache_choices():
    return get_caches()


class SearchForm(forms.Form):
    cache = forms.ChoiceField(
        choices=get_cache_choices,
        required=True,
    )
    query = forms.CharField(
        required=True,
        help_text="Comma separated list of terms. For Redis caches, this will search keys. For other caches, this must match the key exactly."
    )
