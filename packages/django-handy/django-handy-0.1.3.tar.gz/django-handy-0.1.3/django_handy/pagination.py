from collections import OrderedDict

from django.core.paginator import Paginator as DjangoPaginator
from django.utils.functional import cached_property
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


def _get_count(queryset):
    """Determine an object count, supporting either queryset or regular list. Optimized to use only `id`"""
    try:
        return queryset.values('id').count()
    except (AttributeError, TypeError):
        return len(queryset)


class ModifiedDjangoPaginator(DjangoPaginator):
    @cached_property
    def count(self):
        return _get_count(self.object_list)


class DefaultPaginator(PageNumberPagination):
    """Use optimized .count() and add page number to response"""
    page_size = 20
    django_paginator_class = ModifiedDjangoPaginator

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page', self.page.number),
            ('results', data)
        ]))


class LimitOffsetPaginator(LimitOffsetPagination):
    """Use optimized .count()"""
    default_limit = 6

    def get_count(self, queryset):
        return _get_count(queryset)
