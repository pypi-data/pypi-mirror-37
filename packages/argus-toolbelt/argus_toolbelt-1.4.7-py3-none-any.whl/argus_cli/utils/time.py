"""Utility functions for parsing and formating time in plugins"""
import time
from datetime import datetime, timedelta


def date_or_relative(input):
    """Convince function that merges date-time and time diff formats"""
    try:
        return date_time_to_timestamp(input)
    except ValueError:
        return int(time.time() * 1e3 - time_diff(input))


def date_time_to_timestamp(input):
    """Parses a time argument in a ISO8601 format

    Can either be just date, or date + time
    """
    if input == "now":
        return int(time.mktime(datetime.now().timetuple()) * 1e3)  # Add milliseconds

    if len(input) is len("YYYY-mm-dd"):
        time_format = "%Y-%m-%d"
    elif len(input) is len("YYYY-mm-ddTHH-MM-SS"):
        if 'T' in input:
            time_format = "%Y-%m-%dT%H:%M:%S"
        else:
            # Someone might send a more human readable input
            time_format = "%Y-%m-%d %H:%M:%S"
    elif input == "now":
        return int(time.mktime(datetime.now().timetuple()) * 1e3)  # Add milliseconds
    else:
        raise ValueError("Invalid time input-format. Use ISO8601 format")
    date = datetime.strptime(input, time_format)
    return int(time.mktime(date.timetuple()) * 1e3)


def time_diff(input):
    """Converts the input from one unit to milliseconds"""
    units = {"s": 1, "m": 60, "h": 60 * 60, "d": 60 * 60 * 24, "w": 60 * 60 * 24 * 7}
    if input == "now":
        return 0
    else:
        return int(input[:-1]) * units[input[-1]] * 1000


def timestamp_to_period(timestamp: int):
    """Converts a timestamp to a ISO8601 style period with days"""
    clock_time = datetime.utcfromtimestamp(timestamp)
    return "P{days:03}DT{hours:02}:{minutes:02}:{seconds:02}".format(
        days=timedelta(seconds=timestamp).days,
        hours=clock_time.hour, minutes=clock_time.minute, seconds=clock_time.second
    )


def timestamp_to_date(timestamp: int):
    """Converts a timestamp to a ISO8601 style date and time"""
    return datetime.fromtimestamp(timestamp).isoformat()
