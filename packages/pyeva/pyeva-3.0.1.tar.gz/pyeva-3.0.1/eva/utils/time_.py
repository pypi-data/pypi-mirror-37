# pylint: disable=C0103

import time
import datetime


def after_days(days):
    '''返回指定天数后的时间

    '''

    now = datetime.datetime.utcnow()
    return now + datetime.timedelta(days=days)


def after_seconds(seconds):
    '''返回指定秒数后的时间

    '''

    now = datetime.datetime.utcnow()
    return now + datetime.timedelta(seconds=seconds)


def datetime_to_seconds(dt):
    '''转换 datetime 时间为秒（UNIX）
    '''
    return int(time.mktime(dt.timetuple()))


def seconds_to_datetime(seconds):
    '''转换 UNIX timestamp 为 datetime 对象
    '''
    return datetime.datetime.fromtimestamp(seconds)


def rfc3339_string(t):
    '''转化 datetime 为 rfc3339 格式字符串'''
    return t.isoformat('T') + 'Z'


def utc_rfc3339_string(dt):
    '''转化 datetime(UTC) 为 rfc3339 格式字符串'''

    return dt.isoformat('T') + 'Z'


def utc_rfc3339_parse(s):
    '''转化 rfc3339 (UTC) 格式字符串为 datetime'''

    if not s:
        return None
    if s[-1].upper() != 'Z':
        return None
    if '.' in s:
        return datetime.datetime.strptime(s.rstrip('Zz'), '%Y-%m-%dT%H:%M:%S.%f')

    return datetime.datetime.strptime(s.rstrip('Zz'), '%Y-%m-%dT%H:%M:%S')


def rfc3339_string_utcnow():
    return datetime.datetime.utcnow().isoformat('T') + 'Z'
