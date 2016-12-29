
import pytest

from jirareports import metrics

# ==========================================================================================
#
#   MetricsStorage
#
#

def test_metrics_storage_create():

    m = metrics.MetricsStorage()
    assert isinstance(m, metrics.MetricsStorage)

    m = metrics.MetricsStorage([
        {'datetime': '2016-12-20', 'value': 1},
        {'datetime': '2016-12-20', 'value': 1},
        {'datetime': '2016-12-20', 'value': 1},
    ])
    assert isinstance(m, metrics.MetricsStorage)


def test_metrics_storage_groupby():

    m = metrics.MetricsStorage([
        {'datetime': '2016-12-20', 'value': 1},
        {'datetime': '2016-12-20', 'value': 1},
        {'datetime': '2016-12-20', 'value': 1},
    ])
    assert list(m.groupby()) == [{'datetime': '2016-12-20', 'value': 3}]


def test_metrics_storage_add():

    m = metrics.MetricsStorage()
    m.add({'datetime': '2016-12-20', 'value': 1})
    m.add([
        {'datetime': '2016-12-20', 'value': 1},
        {'datetime': '2016-12-20', 'value': 1},
    ])
    assert list(m.groupby()) == [{'datetime': '2016-12-20', 'value': 3}]

    with pytest.raises(RuntimeError):
        m.add([('datetime', '2016-12-20'), ('value', 1),])


def test_metrics_storage_filter():

    m = metrics.MetricsStorage([
        {'datetime': '2016-12-21', 'value': 1},
        {'datetime': '2016-12-22', 'value': 1},
        {'datetime': '2016-12-23', 'value': 1},
        {'datetime': '2016-12-24', 'value': 1},
    ])
    assert m.filter('2016-12-22', '2016-12-23').json() == metrics.MetricsStorage([
        {'datetime': '2016-12-22', 'value': 1},
        {'datetime': '2016-12-23', 'value': 1},
    ]).json()


def test_metrics_storage_conv():

    m = metrics.MetricsStorage([
        {'datetime': 1482100650, 'value': 1},
        {'datetime': 1482960650, 'value': 1},
    ])
    assert m.conv(roundto=86400).json() == metrics.MetricsStorage([
        {'datetime': '2016-12-18', 'value': 1},
        {'datetime': '2016-12-28', 'value': 1},
    ]).json()

# ==========================================================================================
#
#   MetricsProcessor
#
#

def test_metrics_processor_create(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-metrics-processor-create'))
    p = metrics.MetricsProcessor(pattern='test', path=tmp_path)

    assert p.path == tmp_path
    assert isinstance(p, metrics.MetricsProcessor)
    assert isinstance(p.metrics(), metrics.MetricsStorage)

    with pytest.raises(IOError):
        p = metrics.MetricsProcessor(pattern='test')

# ==========================================================================================
#
#   SimpleMetric
#
#

def test_simple_metric_create(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-simple-metric-create'))
    m = metrics.SimpleMetric(pattern='test', path=tmp_path)
    assert isinstance(m, metrics.SimpleMetric)


def test_simple_metric_add_event(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-simple-metric-add-event'))
    m = metrics.SimpleMetric(pattern='test', path=tmp_path)
    assert m.add_event({'test': 1482960650}) == [{'datetime': 1482960600, 'value': 1},]

# ==========================================================================================
#
#   EdgeMetric
#
#

def test_edge_metric_create(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-edge-metric-create'))
    m = metrics.EdgeMetric(pattern='test', path=tmp_path)
    assert isinstance(m, metrics.EdgeMetric)

    with pytest.raises(RuntimeError):
        m = metrics.EdgeMetric(pattern='test', path=tmp_path, select='something')


def test_edge_metric_add_event(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-edge-metric-add-event'))
    m = metrics.EdgeMetric(pattern='test', path=tmp_path)

    # key/value, where value is integer
    assert m.add_event({'test': 1482960650}) == []

    # key/value, where value is the list of (dt_start, dt_end, value)
    assert m.add_event({'test': [(1482960650, 148296065, 'value')]}) == []


def test_edge_metric_add_event_last_left(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-edge-metric-add-event-last-left'))
    m = metrics.EdgeMetric(pattern='test', path=tmp_path, select='last-left', includes=('value',), roundto=900)

    assert m.add_event(
                    {'test': [(1482960000, 1482970000, 'value')]}
                ) == [{'datetime': 1482959700, 'value': 1}]

    assert m.add_event(
                    {'test': [(1482950000, 1482960000, 'value'), (1482960000, 1482970000, 'value')]},
                ) == [{'datetime': 1482959700, 'value': 1}]

    m = metrics.EdgeMetric(pattern='test', path=tmp_path, select='last-left', excludes=('value',), roundto=900)

    assert m.add_event({'test': [(1482960000, 1482970000, 'value')]}) == []
    assert m.add_event({'test': [(1482950000, 1482960000, 'value'), (1482960000, 1482970000, 'value')]},) == []

# ==========================================================================================
#
#   RangeMetric
#
#
def test_range_metric_add_event(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-range-metric-add-event'))
    m = metrics.RangeMetric(pattern='test', path=tmp_path, roundto=900, includes=('value',))

    # key/value, where value is the list of (dt_start, dt_end, value)
    for p in m.add_event({'test': [(1482960000, 1482965000, 'value')]}):
        assert p in [
                        {'datetime': 1482959700, 'value': 1},
                        {'datetime': 1482960600, 'value': 1},
                        {'datetime': 1482961500, 'value': 1},
                        {'datetime': 1482962400, 'value': 1},
                        {'datetime': 1482963300, 'value': 1},
                        {'datetime': 1482964200, 'value': 1},
                    ]

# ==========================================================================================
#
#   MultiPatternMetric
#
#

def test_multi_pattern_metric_create(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-multi-pattern-metric-create'))
    m = metrics.MultiPatternMetric(
                    metrics.RangeMetric(pattern='test1', path=tmp_path, roundto=900, includes=('value1',)),
                    metrics.RangeMetric(pattern='test2', path=tmp_path, roundto=900, includes=('value2',))
    )
    assert isinstance(m, metrics.MultiPatternMetric)


def test_multi_pattern_metric_add_event(tmpdir):

    tmp_path = str(tmpdir.mkdir('test-multi-pattern-metric-add-event'))
    m = metrics.MultiPatternMetric(
                    metrics.RangeMetric(pattern='test1', path=tmp_path, roundto=900, includes=('value1',)),
                    metrics.RangeMetric(pattern='test2', path=tmp_path, roundto=900, includes=('value2',))
    )

    for p in m.add_event({'test1': [(1482960000, 1482965000, 'value1')],'test2': [(1482960000, 1482962000, 'value2')],}):
        assert p in [
                        {'datetime': 1482959700, 'value': 1},
                        {'datetime': 1482960600, 'value': 1},
                        {'datetime': 1482961500, 'value': 1},
        ]
