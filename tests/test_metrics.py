
import pytest

from jirareports import metrics

def test_dt_round_value():

    DATETIME = 1452552920
    assert (
        metrics.dt(DATETIME), metrics.dt_round(DATETIME, 900),
        metrics.dt_round(DATETIME, 3600), metrics.dt_round(DATETIME, 86400),
    ) == (
        '2016-01-11 22:55:20', '2016-01-11 22:45',
        '2016-01-11 22', '2016-01-11',
    )
    DATETIME = 1452063983
    assert (
        metrics.dt(DATETIME), metrics.dt_round(DATETIME, 900),
        metrics.dt_round(DATETIME, 3600), metrics.dt_round(DATETIME, 86400),
    ) == (
        '2016-01-06 07:06:23', '2016-01-06 07:00',
        '2016-01-06 07', '2016-01-06',
    )
    DATETIME = 1458832665
    assert (
        metrics.dt(DATETIME), metrics.dt_round(DATETIME, 900),
        metrics.dt_round(DATETIME, 3600), metrics.dt_round(DATETIME, 86400),
    ) == (
        '2016-03-24 15:17:45', '2016-03-24 15:15',
        '2016-03-24 15', '2016-03-24',
    )

def test_dt_round_interval():

    TIME_INTERVALS = (1452552920, 1453552920)
    # TODO: add test cases for handling time intervals
