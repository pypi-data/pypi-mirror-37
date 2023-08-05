from django.utils import timezone


SATURDAY = 5


def add_business_days(date, days):
    one_day = timezone.timedelta(days=1)
    while days > 0:
        date += one_day
        weekday = date.weekday()
        if weekday >= SATURDAY:
            continue
        days -= 1
    return date
