from datetime import date, datetime


def rus_datetime_fmt(value: datetime | date):
    """
    Russian date and datetime format template filter for Jinja2
    """
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y %H:%M")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
