
import re
import json
import logging
import datetime

import operator
import itertools


logger = logging.getLogger(__name__)

def dt(epochtime):
    ''' returns epoch time in %Y-%m-%d %H:%M:%S format
    '''
    dt_format = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.fromtimestamp(epochtime).strftime(dt_format)


def dt_round(epochtime, roundto=None):
    ''' return rounded epoch time to 'roundto' value and format to the next formats:
    # - %Y-%m-%d %H:%M:%S
    # - %Y-%m-%d %H:%M
    # - %Y-%m-%d %H
    # - %Y-%m-%d
    '''
    dt_format = '%Y-%m-%d %H:%M:%S'
    if roundto >= 86400:
        dt_format = '%Y-%m-%d'
    elif roundto >= 3600:
        dt_format = '%Y-%m-%d %H'
    elif roundto >= 60:
        dt_format = '%Y-%m-%d %H:%M'
    dt = epochtime - epochtime % roundto
    return datetime.datetime.fromtimestamp(dt).strftime(dt_format)


class MetricsProcessor(object):

    def __init__(self, name, key_pattern, value=None, roundto=900):

        self._name = name
        self._key_pattern = re.compile(key_pattern)
        self._value = value
        self._roundto = roundto
        self._metrics = list()

    def add_event(self, fields):

        for k,value in fields.items():
            if self._key_pattern.search(k):
                if isinstance(value, int):
                    self._metrics.append({'datetime': dt_round(value, self._roundto), 'value': 1})
                elif isinstance(value, list):
                    print "\t", [v for v in value if v[2].lower() == self._value.lower()]
                else:
                    logger.error('Unknown value type: %s' % type(value))

    def process(self):

        self._metrics.sort(key=operator.itemgetter('datetime'))
        for dt, items in itertools.groupby(self._metrics, key=operator.itemgetter('datetime')):
            yield {'datetime': dt, 'value': sum([i['value'] for i in items]) }

    def metrics(self):
        ''' returns metrics
        '''
        return self._metrics


    def json(self):
        ''' returns metrics in JSON format
        '''
        return json.dumps([v for v in self.process()])
