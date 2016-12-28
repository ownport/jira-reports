
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
