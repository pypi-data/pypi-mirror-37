import re
from decimal import Decimal

from .helpers import d_round


not_human_chars = re.compile('([_.])')


def humanize(origin: str) -> str:
    """
        Converts string to be more human-readable.
        Replaces dots and underscores with spaces, capitalize result.
        Can be used to display model fields names to user. (similar to django admin)
    """
    humanized = not_human_chars.sub(' ', origin).strip()
    return humanized.capitalize()


def strip_zeros(val, keep=0):
    """
        Strips trailing zeros but keeps at least `keep` zeros

        strip_zeros(12, 2) -> 12.00
        strip_zeros(12.00) -> 12
        strip_zeros(12.001, 2) -> 12.001

    """
    if val is None:
        return None

    # Strip redundant zeros
    d = Decimal(val)
    normalized = d.normalize()

    # Remove scientific notation, i.e. convert 5.6e+2 to 560
    sign, digit, exponent = normalized.as_tuple()
    non_scientific = normalized if exponent <= 0 else normalized.quantize(1)

    with_zeros = d_round(non_scientific, keep)
    # If rounding doesn't change value, it means we append zeros as desired
    # Otherwise it removes non-zero numbers, so we won't apply rounding and keep received precision
    if non_scientific == with_zeros:
        non_scientific = with_zeros
    return non_scientific
