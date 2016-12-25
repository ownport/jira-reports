
import pytest

from jirareports import dt

def test_epoch2dt():

    assert dt.epoch2dt(1452552920) == '2016-01-11 22:55:20'


def test_dt_roundto():

    DATETIME = 1452552920
    assert dt.roundto(DATETIME, 900) == 1452552300
    assert dt.roundto(DATETIME, 3600) == 1452549600
    assert dt.roundto(DATETIME, 86400) == 1452470400

    DATETIME = 1452063983
    assert dt.roundto(DATETIME, 900) == 1452063600
    assert dt.roundto(DATETIME, 3600) == 1452063600
    assert dt.roundto(DATETIME, 86400) == 1452038400

    DATETIME = 1458832665
    assert dt.roundto(DATETIME, 900) == 1458832500
    assert dt.roundto(DATETIME, 3600) == 1458831600
    assert dt.roundto(DATETIME, 86400) == 1458777600


def test_dt_roundto_range():

    assert dt.roundto_range(1452552920, 1452559920, 3600) == [1452549600, 1452553200, 1452556800]
    assert dt.dt_format(1452552920, 0) == '2016-01-11 22:55:20'
    assert dt.dt_format(1452559920, 0) == '2016-01-12 00:52:00'

    assert dt.dt_format(1452549600, 3600) == '2016-01-11 22'
    assert dt.dt_format(1452553200, 3600) == '2016-01-11 23'
    assert dt.dt_format(1452556800, 3600) == '2016-01-12 00'

    assert dt.roundto_range(1481021241, 1481022405, 86400) == [1480982400,]
    assert dt.roundto_range(1481023163, 1481078848, 86400) == [1480982400, 1481068800,]
