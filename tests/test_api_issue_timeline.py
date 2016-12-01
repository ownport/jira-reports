
import pytest

from jirareports import api
from jirareports.utils import optimize_timeintervals


TIME_INTERVALS_01 = [
    [1477638026, 1478673745, None, u'user1'],
    [1477638026, 1477643257, u'user2', u'user3'],
    [1477643257, 1477645487, u'user3', u'user1'],
    [1477645487, 1477645800, u'user1', u'user3'],
    [1477645800, 1477648593, u'user3', u'user1'],
    [1477648593, 1477649462, u'user1', u'user2'],
    [1477649462, 1477649787, u'user2', u'user4'],
    [1477649787, 1478649405, u'user4', u'user5'],
    [1478649405, 1478651945, u'user5', u'user1'],
]

TIME_INTERVALS_02 = [
    [1479804035, 1480338303, None, u'Closed'],
    [1479804035, 1479886006, u'Open', u'In Progress'],
    [1479886006, 1480316092, u'In Progress', u'Open'],
    [1480316092, 1480317511, u'Open', u'In Progress'],
    [1480317511, 1480338304, u'In Progress', u'Closed']
]

TIME_INTERVALS_03 = [
    [1479804035, 1480338303, None, u'2016-11-28'],
    [1480338303, 1480338304, None, u'28/Nov/16']
]

FIELDS_SAMPLE = {
    u'status': [
        (1449084416, None, None),
        (1473161751, None, u'Closed'),
        (1449158492, u'Open', u'Resolved'),
        (1449159411, u'Resolved', u'Closed'),
        (1453240059, u'Closed', u'Resolved'),
        (1473161751, u'Resolved', u'Closed')
    ],
}


def test_api_issue_timeline_experiment_01():
    ''' create the list of intervals for each value
    '''
    _time_intervals = list(TIME_INTERVALS_01)

    duration, result = optimize_timeintervals(_time_intervals)

    assert duration == 0
    assert result == [
        [1477638026, 1477643257, u'user2'],
        [1477643257, 1477645487, u'user3'],
        [1477645487, 1477645800, u'user1'],
        [1477645800, 1477648593, u'user3'],
        [1477648593, 1477649462, u'user1'],
        [1477649462, 1477649787, u'user2'],
        [1477649787, 1478649405, u'user4'],
        [1478649405, 1478651945, u'user5'],
        [1478651945, 1478673745, u'user1'],
    ]

def test_api_issue_timeline_experiment_02():
    ''' create the list of intervals for each value
    '''
    _time_intervals = list(TIME_INTERVALS_02)

    duration, result = optimize_timeintervals(_time_intervals)

    print 'Source time intervals:', TIME_INTERVALS_02
    print 'Result time intervals:', result
    assert duration in [0, -1]
    assert result == [
        [1479804035, 1479886006, u'Open'],
        [1479886006, 1480316092, u'In Progress'],
        [1480316092, 1480317511, u'Open'],
        [1480317511, 1480338304, u'In Progress']
    ]

def test_api_issue_timeline_experiment_03():
    ''' create the list of intervals for each value
    '''
    return
    _time_intervals = list(TIME_INTERVALS_03)

    duration, result = optimize_timeintervals(_time_intervals)

    print 'Source time intervals:', TIME_INTERVALS_03
    print 'Result time intervals:', result
    assert duration in [0, -1]
    assert result == [
    ]
