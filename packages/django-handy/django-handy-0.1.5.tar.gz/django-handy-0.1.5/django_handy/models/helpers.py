from typing import List, Type

from django.db import models
from django.db.models.options import Options
from manager_utils import bulk_upsert as original_bulk_upsert

from ..helpers import get_unique_objs


def get_bulk_update_fields(cls: Type[models.Model], unique_fields: List[str] = None) -> List[str]:
    """
        Return list of all model fields that can be updated in bulk,
        excluding fields used as unique constraints
    """
    if unique_fields is None:
        unique_fields = get_unique_fields(cls)

    def _should_be_updated(field):
        return (
            field.name not in unique_fields and
            not (field.many_to_many or field.one_to_many)
        )

    return [
        field.name for field in cls._meta.get_fields()
        if _should_be_updated(field)
    ]


def get_unique_fields(cls: Type[models.Model]) -> List[str]:
    """
        Useful in cases of some unique collection of related instances,
        i.e. Product with multiple Variation, where Variation.name should be unique across single Product.

        class Variation:
            name = models.CharField(...)
            product = models.ForeignKey(...)

            class Meta
                unique_together = ('product', 'name')

        get_unique_fields(Variation) -> ('product', 'name')
    """
    opts: Options = cls._meta
    if opts.unique_together and len(opts.unique_together) == 1:
        return opts.unique_together[0]
    raise ValueError(f'{cls}.Meta must declare exactly one unique_together.')


def is_editable(f: models.Field):
    return f.editable and not f.auto_created


def bulk_upsert(
    queryset: models.QuerySet, model_objs: List[models.Model],
    unique_fields: List[str], update_fields: List[str] = None,
    return_upserts: bool = False, return_upserts_distinct: bool = False,
    sync: bool = False, native: bool = False
):
    """Type mismatch fixing"""
    # noinspection PyTypeChecker
    return original_bulk_upsert(
        queryset,
        model_objs=model_objs,
        unique_fields=unique_fields,
        update_fields=update_fields,
        return_upserts=return_upserts,
        return_upserts_distinct=return_upserts_distinct,
        sync=sync,
        native=native
    )


def safe_bulk_upsert(
    queryset: models.QuerySet, model_objs: List[models.Model],
    unique_fields: List[str], update_fields: List[str] = None,
    return_upserts: bool = False, return_upserts_distinct: bool = False,
    sync: bool = False, native: bool = False
):
    """
        Removes objs with duplicate unique fields to prevent IntegrityError.
        Uses first unique obj encountered
    """
    # noinspection PyTypeChecker
    return bulk_upsert(
        queryset,
        model_objs=get_unique_objs(model_objs, unique_fields),
        unique_fields=unique_fields,
        update_fields=update_fields,
        return_upserts=return_upserts,
        return_upserts_distinct=return_upserts_distinct,
        sync=sync,
        native=native
    )
