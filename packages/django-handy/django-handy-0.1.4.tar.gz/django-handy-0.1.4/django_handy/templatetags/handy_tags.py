from django import template
from django.utils.safestring import mark_safe

from ..format import humanize, strip_zeros
from ..helpers import is_empty


register = template.Library()


@register.filter
def or_dash(value):
    if is_empty(value):
        return '-'
    return value


@register.filter(name='strip_zeros')
def strip_zeros_filter(val, keep=0):
    if is_empty(val):
        return ''

    return str(strip_zeros(val, keep=keep))


@register.filter(name='humanize')
def humanize_filter(field_name):
    return humanize(field_name)


@register.simple_tag
def mailto(address, text=None):
    return mark_safe(
        f'<a href="mailto:{address}">{text or address}</a>'
    )
