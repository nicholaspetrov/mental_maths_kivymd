from datetime import datetime


def get_string_for_datetime(d=None):
    if not d:
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return d.strftime('%Y-%m-%d %H:%M:%S')


def get_date_string_for_datetime(d):
    return d.strftime('%y-%m-%d %H:%M')


def get_datetime_for_string(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

