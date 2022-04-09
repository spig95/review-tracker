import datetime
import time

from scrape_app.utility.logger import log


def get_timestamp(year, month, day):
    """Get timestamp from year, month, day

        >>> ts = get_timestamp(2020, 1, 1)
        >>> print(ts) # 1577833200.0
    """
    dt = datetime.datetime(year=year, month=month, day=day)
    timestamp = time.mktime(dt.timetuple())
    return timestamp


def get_date(timestamp):
    """Get year, month, day from timestamp

        >>> y, m, d = get_date(1577833200)
        >>> print(y, m, d) # 2020, 1, 1
    """
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    return dt_obj.year, dt_obj.month, dt_obj.day


def get_days_difference(ts1, ts2):
    """Get how many days have elapsed between timestamp 1  (ts1) and timestamp 2 (ts2)

        >>> ts1 = get_timestamp(2021, 1, 30)
        >>> ts2 = get_timestamp(2022, 1, 30)
        >>> diff = get_days_difference(ts1, ts2)
        >>> print(diff) # 365
    """
    diff = abs(ts1 - ts2)
    # Diff is in seconds, convert it into days
    days_diff = round(diff / 60 / 60 / 24)
    return days_diff


def order_by_time(timestamps, values):
    """Sort based on timestamps"""
    if len(timestamps) and len(values):
        timestamps, values = (list(t) for t in zip(*sorted(zip(timestamps, values))))
    else:
        log.warning("Got empty timestamps or values")
    return timestamps, values
