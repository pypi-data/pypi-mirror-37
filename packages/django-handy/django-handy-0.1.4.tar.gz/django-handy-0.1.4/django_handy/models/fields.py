# django.contrib.postgres requires psycopg2
try:
    from django.contrib.postgres.fields import ArrayField
except ImportError:
    ArrayField = None

from django.core.validators import MinValueValidator
from django.db import models

from ..helpers import unique_ordered


class PositiveDecimalField(models.DecimalField):
    default_validators = [MinValueValidator(0)]


if ArrayField:
    class UniqueArrayField(ArrayField):
        """Ensures that no duplicates are saved to database"""

        def get_db_prep_value(self, value, connection, prepared=False):
            if isinstance(value, (list, tuple)):
                value = unique_ordered(value)
            return super().get_db_prep_value(value, connection, prepared)
