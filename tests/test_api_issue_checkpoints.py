
import pytest

from jirareports import api
from jirareports.utils import optimize_checkpoints
from jirareports.utils import create_timeintervals


STATUS_CHECKPOINTS = [
    (1449084416, None, None),
    (1473161751, None, u'Closed'),
    (1480633671, u'Closed', None),
    (1449158492, u'Open', u'Resolved'),
    (1449159411, u'Resolved', u'Closed'),
    (1453240059, u'Closed', u'Resolved'),
    (1473161751, u'Resolved', u'Closed')
]

FIELDS_SAMPLE = {
    u'status': STATUS_CHECKPOINTS,
}


def test_utils_optimize_checkpoints():

    checkpoints = optimize_checkpoints(FIELDS_SAMPLE[u'status'])
    assert checkpoints == []


def test_utils_create_timeintervals():

    timeintervals = create_timeintervals(FIELDS_SAMPLE[u'status'])
    assert timeintervals == [
        (1449084416, 1449158492, 'Open'),
        (1449158492, 1449159411, 'Resolved'),
        (1449159411, 1453240059, 'Closed'),
        (1453240059, 1473161751, 'Resolved'),
        (1473161751, 1480633671, 'Closed'),
    ]
