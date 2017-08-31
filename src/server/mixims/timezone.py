import pytz
from dateutil import parser
from app import app
from datetime import datetime, timedelta, tzinfo, time

ZERO = timedelta(0)


class UTC(tzinfo):
    """
    UTC implementation taken from Python's docs.

    Used only when pytz isn't available.
    """

    def __repr__(self):
        return "<UTC>"

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = pytz.utc if pytz else UTC()
"""UTC time zone as a tzinfo instance."""


def now():
    """
    Returns an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    if app.config['USE_TZ']:
        # timeit shows that datetime.now(tz=utc) is 24% slower
        return datetime.utcnow().replace(tzinfo=utc)
    else:
        return datetime.now()


def get_week_range(date):
    """
    Find the first/last day of the week for the given day. Assuming weeks start on
    Sunday and end on Saturday.

    :param date
        The date to use to get the week range.

    :returns:
        A tuple of ``(start_datetime, end_datetime)``.
    """
    # isocalendar calculates the year, week of the year, and day of the week.
    # dow is Mon = 1, Sat = 6, Sun = 7
    year, week, dow = date.isocalendar()

    # Find the first day of the week.
    if dow == 7:
        # Since we want to start with Sunday, let's test for that condition.
        start_date = date
    else:
        # Otherwise, subtract `dow` number days to get the first day
        start_date = date - timedelta(dow)

    # Now, add 6 for the last day of the week (i.e., count up to Saturday)
    end_date = start_date + timedelta(6)

    # Add time.
    start_date = datetime.combine(start_date, time())
    end_date = datetime.combine(end_date, time(23, 59, 59))

    return pytz.utc.localize(start_date), pytz.utc.localize(end_date)


def get_week_range_from_week(year, week, company):
    """
    Function to calculate date range of a week, given the week and the year. Assuming weeks start on
    Sunday and end on Saturday.

    :param year:
    :param week:
    :param company:
    :return: date range of the given week in the year, in the users company timezone
    """
    d = datetime(year, 1, 1, tzinfo=company.timezone)
    if d.weekday() > 3:
        d = d+timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days=((week-1)*7)-1)
    return d + dlt,  d + dlt + timedelta(days=6)
