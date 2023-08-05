from functools import wraps

from ..helpers import all_not_empty, get_attribute


def calculated_field(*required_fields, forbid_zero=False):
    """
    Ensures that all specified fields are available so it is safe to use them in calculations
    """

    def decorator(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            if not all_not_empty(self, *required_fields):
                return None

            if forbid_zero:
                if any(get_attribute(self, field) == 0 for field in required_fields):
                    return None

            return func(self, *args, **kwargs)

        return property(wrapped)

    return decorator
