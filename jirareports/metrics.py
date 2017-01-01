
import os
import re
import json
import logging

import operator
import itertools
import collections

import dt

logger = logging.getLogger(__name__)


class MetricsStorage(object):
    '''
    <datetime>: <value>
    '''

    def __init__(self, metrics=list()):

        self._metrics = list()
        if metrics:
            self._metrics = metrics


    def groupby(self):

        # TODO change to use defaultdict
        self._metrics.sort(key=operator.itemgetter('datetime'))
        for dt, items in itertools.groupby(self._metrics, key=operator.itemgetter('datetime')):
            yield {'datetime': dt, 'value': sum([i['value'] for i in items]) }


    def add(self, metrics):
        ''' add metrics
        '''
        # store one metric
        if isinstance(metrics, dict):
            self._metrics.append(metrics)

        # store the list of metrics
        elif isinstance(metrics, list):
            for metric in metrics:
                if not isinstance(metric, dict):
                    raise RuntimeError('Unknown metric type, %s' % type(metric))
                self._metrics.append(metric)


    def filter(self, date_from, date_to):
        ''' filter metrics by date range
        '''
        result = [
            metric for metric in self.groupby() if metric[u'datetime'] >= date_from and metric[u'datetime'] <= date_to
        ]
        return MetricsStorage(metrics=result)

    def conv(self, roundto):
        ''' convert datetime key (epochtime) according to roundto parameter
        '''
        result = [
            {
                'datetime': dt.dt_format(metric['datetime'], roundto=roundto),
                'value': metric['value']
            } for metric in self.groupby()
        ]
        return MetricsStorage(metrics=result)

    def items(self):

        return self._metrics


    def json(self):
        ''' returns metrics in JSON format
        '''
        return json.dumps([v for v in self.groupby()])


# class MetricsProcessor(object):
#
#     def __init__(self, key_pattern, value=None, roundto=900):
#
#         self._key_pattern = re.compile(key_pattern)
#         self._value = value
#         self._storage = MetricsStorage()
#
#         self.roundto = roundto
#
#     def metrics(self):
#
#         return self._storage


class MetricsProcessor(object):

    def __init__(self, pattern, includes=(), excludes=(), roundto=900, path=None):

        self._pattern = re.compile(pattern)
        if not isinstance(includes, (list, tuple)):
            raise RuntimeError('Incorrect includes type: %s' % type(includes))
        if not isinstance(excludes, (list, tuple)):
            raise RuntimeError('Incorrect excludes type: %s' % type(excludes))
        self._includes = [v.lower() for v in includes]
        self._excludes = [v.lower() for v in excludes]
        self._storage = MetricsStorage()

        if not path or not os.path.exists(path):
            raise IOError('The path to the metrics does not exist, %s' % path)
        self._path = path

        self.roundto = roundto

    @property
    def path(self):
        return self._path

    def metrics(self):
        return self._storage

    def __str__(self):
        return "%s(pattern=%s,includes=%s,excludes=%s)" % (
                    self.__class__,
                    self._pattern.pattern,
                    self._includes,
                    self._excludes
        )


class SimpleMetric(MetricsProcessor):
    ''' Simple metric

    count issues with specific parameter value only
    '''
    def add_event(self, fields):

        _result = list()
        for k,value in fields.items():
            if self._pattern.search(k):

                # is it really needed?

                # if self._includes and value not in self._includes:
                #     continue
                # if self._excludes and value in self._excludes:
                #     continue

                _result.append({'datetime': dt.roundto(value, self.roundto), 'value': 1})

        self._storage.add(_result)
        return _result


class EdgeMetric(MetricsProcessor):
    ''' Edge metric

    count issues where selected parameter can be provided as the list with ranges. For example:

    [(1463075452, 1463599017, u'Closed'), (1463675880, 1480841839, u'Closed')]

    Possible options:
    - last-right (implemented)
    - last-left
    - first-right
    - first-left
    '''
    def __init__(self, pattern, includes=(), excludes=(), roundto=900, select=None, path=None):

        super(EdgeMetric, self).__init__(pattern, includes, excludes, roundto, path)
        self._select = None
        if select and select not in ('last-left', 'last-right', 'first-left', 'first-right'):
            raise RuntimeError('Unknown value for select parameter: %s' % select)
        else:
            self._select = select

    def add_event(self, fields):

        _result = list()
        for k,value in fields.items():
            if self._pattern.search(k):
                if isinstance(value, list):
                    _values = [v for v in value if self._includes and v[2].lower() in self._includes]
                    _values += [v for v in value if self._excludes and v[2].lower() not in self._excludes]
                    if _values and self._select == 'last-left':
                        _result.append({'datetime': dt.roundto(_values[-1][0] or None, self.roundto), 'value': 1})
        self._storage.add(_result)
        return _result


class RangeMetric(MetricsProcessor):
    ''' Range Metric

    count issues in range interval_start..interval_end for (interval_start, interval_end, value)
    '''
    def add_event(self, fields):

        _result = list()
        for k,value in fields.items():
            if self._pattern.search(k):
                if isinstance(value, list):
                    _values = [v for v in value if self._includes and v[2].lower() in self._includes]
                    _values += [v for v in value if self._excludes and v[2].lower() not in self._excludes]
                    _dts = list()
                    for v in _values:
                        _dts += [t for t in dt.roundto_range(v[0], v[1], self.roundto)]
                    _result += [{'datetime': d, 'value': 1} for d in set(_dts)]
        self._storage.add(_result)
        return _result


class MultiPatternMetric(object):

    def __init__(self, *processors):

        self._processors = processors
        self.roundto = list(set([proc.roundto for proc in self._processors]))[0]
        self.path = list(set([proc.path for proc in self._processors]))[0]
        self._storage = MetricsStorage()

    def add_event(self, fields):

        grouped_metrics = collections.defaultdict(list)
        for proc in self._processors:
            for kv in proc.add_event(fields):
                grouped_metrics[kv['datetime']].append(kv['value'])

        _result = map(
                    lambda k: {'datetime': k, 'value': 1},
                    filter(lambda k: len(grouped_metrics[k]) == len(self._processors), grouped_metrics)
        )
        self._storage.add(_result)
        return _result


    def metrics(self):

        return self._storage


def get_metric_processors(metrics):

    # TODO: !!! optimize selection of metrics processors

    _result = {}
    for m in metrics:
        if m['type'] == 'SimpleMetric':
            _result[m['name']] = SimpleMetric(
                                    pattern=m['pattern'],
                                    roundto=m['roundto'],
                                    path=m['path'])
        elif m['type'] == 'EdgeMetric':
            _result[m['name']] = EdgeMetric(
                                    pattern=m['pattern'],
                                    includes=m.get('includes', []),
                                    excludes=m.get('excludes', []),
                                    roundto=m['roundto'],
                                    select=m['select'],
                                    path=m['path'])
        elif m['type'] == 'RangeMetric':
            _result[m['name']] = RangeMetric(
                                    pattern=m['pattern'],
                                    includes=m.get('includes', []),
                                    excludes=m.get('excludes', []),
                                    roundto=m['roundto'],
                                    path=m['path'])
        elif m['type'] == 'MultiPatternMetric':
            # ONLY RangeMetric processor is supported
            _result[m['name']] = MultiPatternMetric(*[
                                    RangeMetric(
                                        pattern=rm['pattern'],
                                        includes=rm.get('includes', []),
                                        excludes=rm.get('excludes', []),
                                        roundto=rm['roundto'],
                                        path=rm['path']
                                    ) for rm in m['metrics']])
    return _result
