
import pytest

import datetime


def dt(epoch):

    dt_format = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.fromtimestamp(epoch).strftime(dt_format)


def dt_round(dt, roundto=900):

    dt_format = '%Y-%m-%d %H:%M:%S'
    dt = dt - dt % roundto
    return datetime.datetime.fromtimestamp(dt).strftime(dt_format)


def test_groupby_datetime_pattern():

    TIME_INTERVALS = (1452552920, 1453552920)
    assert (
        dt(TIME_INTERVALS[0]), dt_round(TIME_INTERVALS[0], 900),
        dt_round(TIME_INTERVALS[0], 3600), dt_round(TIME_INTERVALS[0], 86400),
    ) == (
        '2016-01-11 22:55:20', '2016-01-11 22:45:00',
        '2016-01-11 22:00:00', '2016-01-11 00:00:00',
    )
    assert (
        dt(TIME_INTERVALS[1]), dt_round(TIME_INTERVALS[1], 900),
        dt_round(TIME_INTERVALS[1], 3600), dt_round(TIME_INTERVALS[1], 86400),
    ) == (
        '2016-01-23 12:42:00', '2016-01-23 12:30:00',
        '2016-01-23 12:00:00', '2016-01-23 00:00:00',
    )
