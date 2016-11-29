
import pytest

from jirareports import api

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


def test_api_issue_timeline_experiment_01():
    ''' create the list of intervals for each value
    '''
    _time_intervals = list(TIME_INTERVALS_01)

    big_ts1, big_ts2, big_val1, big_val2 = _time_intervals.pop(0)
    assert (big_ts1, big_ts2, big_val1, big_val2) == (1477638026, 1478673745, None, u'user1')
    assert len(_time_intervals) == 8

    duration = big_ts2 - big_ts1
    assert duration == 1035719

    result = list()
    while len(_time_intervals) > 0:
        sm_ts1, sm_ts2, sm_val1, sm_val2 = _time_intervals.pop(0)
        if sm_ts1 == big_ts1 and sm_ts2 <= big_ts2:
            big_ts1 = sm_ts2
            result.append([sm_ts1, sm_ts2, sm_val1])
            duration = duration - (sm_ts2 - sm_ts1)
    if big_ts1 >= sm_ts2 and big_ts2 > sm_ts2:
        result.append([big_ts1, big_ts2, big_val2])
        duration = duration - (big_ts2 - big_ts1)

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
