from datetime import datetime


def get_string_for_datetime():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def get_datetime_for_string(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

