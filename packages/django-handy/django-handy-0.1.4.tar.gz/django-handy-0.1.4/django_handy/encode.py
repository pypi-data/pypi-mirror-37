import math
from functools import lru_cache
from itertools import chain
from logging import getLogger

from django.utils.functional import cached_property


""" 
    Credits to https://github.com/simonluijk/django-invoice
    Author: Will Hardy
    Date: December 2008

    These functions convert an integer (from eg an ID AutoField) to a
    short unique string. This is done simply using a perfect hash
    function and converting the result into a string of user friendly
    characters.
"""

logger = getLogger()


class Encoder:
    def __init__(self, size, valid_chars):
        self.size = size
        self.valid_chars = valid_chars

    @classmethod
    @lru_cache(maxsize=10)
    def find_suitable_period(cls, size, valid_chars):
        """
            Automatically find a suitable period to use.
            Factors are best, because they will have 1 left over when
            dividing size+1.
        """
        # The highest acceptable factor will be the square root of the size.
        highest_acceptable_factor = int(math.sqrt(size))

        # Too high a factor (eg size/2) and the interval is too small, too
        # low (eg 2) and the period is too small.
        # We would prefer it to be lower than the number of valid_chars, but more
        # than say 4.
        starting_point = len(valid_chars) > 14 and len(valid_chars) // 2 or 13
        for p in chain(range(starting_point, 7, -1),
                       range(highest_acceptable_factor, starting_point + 1, -1),
                       [6, 5, 4, 3, 2]):
            if size % p == 0:
                return p
        raise ValueError("No valid period could be found for size=%d.\nTry avoiding prime numbers :-)" % size)

    @cached_property
    def period(self):
        return self.find_suitable_period(self.size, self.valid_chars)

    @cached_property
    def offset(self):
        return self.size // 2 - 1

    def perfect_hash(self, num):
        """
            Translate a number to another unique number, using a perfect hash function.
            Only meaningful where 0 <= num <= size.
        """
        return ((num + self.offset) * (self.size // self.period)) % (self.size + 1) + 1

    def friendly_number(self, num):
        """
            Convert a base 10 number to a base X string.
            Charcters from VALID_CHARS are chosen, to convert the number
            to eg base 24, if there are 24 characters to choose from.
            Use valid chars to choose characters that are friendly, avoiding
            ones that could be confused in print or over the phone.
        """
        # Convert to a (shorter) string for human consumption
        string = ''
        while len(self.valid_chars) ** len(string) <= self.size:
            # Prepend string (to remove all obvious signs of order)
            string = self.valid_chars[num % len(self.valid_chars)] + string
            num //= len(self.valid_chars)
        return string

    def encode(self, num):
        """
            Encode a simple number, using a perfect hash and converting to a
            more user friendly string of characters.
        """
        if num is None:
            return None

        if num > self.size:
            raise ValueError(f'Encode numbers is overflowing! Adjust size!')
        if num < 0:
            raise ValueError(f'Number is less then 0')

        if num > self.size - 10000:
            logger.error(f'Encode numbers is going to overflow soon! Adjust size!')

        return self.friendly_number(self.perfect_hash(num))


def encode(num, size=100000000, valid_chars='3456789ACDEFGHJKLQRSTUVWXY'):
    """
        Encode a simple number, using a perfect hash and converting to a
        more user friendly string of characters.
        Generated 6-digits codes by default - up to 100.000.000 of them
    """
    encoder = Encoder(size, valid_chars)
    return encoder.encode(num)
