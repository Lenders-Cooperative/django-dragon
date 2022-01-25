from django import template


register = template.Library()


@register.inclusion_tag('dragon/button.html')
def dragon_cache_manager_button():
    return {}