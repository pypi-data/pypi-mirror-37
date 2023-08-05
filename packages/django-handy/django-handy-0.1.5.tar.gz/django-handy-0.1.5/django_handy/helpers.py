import mimetypes
from collections import Sized
from decimal import Decimal
from functools import wraps
from typing import Dict, Hashable, Iterable, List

import collections
from django.db import transaction
from django.http import HttpResponse
from django.utils.encoding import force_text


def create_attachment_response(filename, content: bytes):
    """
        Creates response to download file with correct headers
         for given content and filename
    """
    response = HttpResponse(content=content)
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    mime_type, encoding = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    response['Content-Type'] = mime_type

    response['Access-Control-Expose-Headers'] = 'Content-Disposition'

    if encoding is not None:
        response['Content-Encoding'] = encoding

    return response


def simple_urljoin(*args):
    """
        Joins url parts like 'https://', 'google.com/', '/search/' to https://google.com/search/

        Treats parts ending on double slash as url beginning and ignores all parts before them.
        Other parts are treated as path and joined with single slash.

        Preserves single trailing and leading slash.
    """
    sep = '/'
    res = ''

    for idx, piece in enumerate(args):
        is_first = idx == 0
        is_last = idx == len(args) - 1

        add_leading_slash = add_trailing_slash = False

        piece = force_text(piece)

        if is_first and piece.startswith(sep):
            add_leading_slash = True

        if is_last and piece.endswith(sep):
            add_trailing_slash = True

        if not is_last:
            add_trailing_slash = True

        piece = piece.strip('/')

        if add_leading_slash:
            piece = sep + piece

        if add_trailing_slash:
            piece += sep

        if '://' in piece:
            res = piece
        else:
            res += piece

    return res


def get_attribute(instance, name):
    """
        Similar to Python's built in `getattr(instance, attr)`,
        but takes a list of nested attributes, instead of a single attribute.

        Also accepts either attribute lookup on objects or dictionary lookups.
    """

    attrs = name.split('.')
    for attr in attrs:
        if isinstance(instance, collections.Mapping):
            try:
                instance = instance[attr]
            except KeyError as exc:
                raise AttributeError(exc) from exc
        else:
            instance = getattr(instance, attr)
    return instance


def has_attribute(obj, name):
    """
        Like normal hasattr, but follows dotted paths
    """
    try:
        get_attribute(obj, name)
    except AttributeError:
        return False

    return True


def bulk_dict_update(dicts_list: List[Dict], update_dict: Dict):
    """As name says, update list of dicts with single dict by calling .update"""
    for dict_ in dicts_list:
        dict_.update(update_dict)


def is_empty(val):
    """
        Check where value is logically `empty` - does not contain information.
        False and 0 are not considered empty, but empty collections are.
    """
    if val is None or isinstance(val, Sized) and len(val) == 0:  # Empty string is also Sized of len 0
        return True
    return False


def all_not_empty(obj, *attrs):
    """
        If all attrs of obj returns False for is_empty check, returns True.
        Otherwise, returns False
    """
    return all(not is_empty(get_attribute(obj, field)) for field in attrs)


def any_not_empty(obj, *attrs):
    """
        If at least one of the attrs of obj returns False for is_empty check, returns True.
        Otherwise, returns False
    """
    return any(not is_empty(get_attribute(obj, field)) for field in attrs)


def join_not_empty(separator, *args):
    """
       Like str.join, but ignores empty values to prevent duplicated separator
    """
    return separator.join(arg for arg in args if not is_empty(arg))


def unique_ordered(sequence: Iterable[Hashable]) -> List:
    """
       Get list of unique values from sequence,
        preserving order when the value first occurred in original sequence
    """
    seen = set()
    unique = []
    for x in sequence:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    return unique


class UpdateDict(dict):
    def __init__(self, update_data, instance):
        super().__init__()
        self.update_data = update_data
        self.instance = instance

    def __getitem__(self, item):
        if item in self.update_data:
            return self.update_data[item]
        return getattr(self.instance, item)

    def get(self, item, default=None):
        try:
            return self[item]
        except AttributeError:
            return default


def get_unique_objs(objs: List[object], unique_attrs: List[str]) -> List[object]:
    """
       Get list of unique objs from sequence,
        preserving order when the objs first occurred in original sequence
    """

    seen_obj_footprints = set()
    unique_objs = []
    for obj in objs:
        obj_footprint = tuple(get_attribute(obj, field) for field in unique_attrs)
        if obj_footprint in seen_obj_footprints:
            continue

        seen_obj_footprints.add(obj_footprint)
        unique_objs.append(obj)
    return unique_objs


def d_round(value, places=2):
    """Decimal version of round() builtin"""
    assert isinstance(places, int)
    quantize_to = Decimal(10) ** (-places)
    return Decimal(value).quantize(quantize_to)


def call_on_commit(func):
    """
        Only call the decorated function at transaction commit.
        The return value will be ignored
    """

    @wraps(func)
    def handle(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return handle
