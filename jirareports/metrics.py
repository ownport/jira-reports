
import re
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


def dt_round(epochtime, roundto=900):
    ''' return rounded epoch time to 'roundto' value and format to the next formats:
    - %Y-%m-%d %H:%M:%S
    # - %Y-%m-%d %H:%M
    # - %Y-%m-%d %H
    # - %Y-%m-%d
    # - %Y-%m
    # - %Y
    '''
    dt_format = '%Y-%m-%d %H:%M:%S'
    dt = epochtime - epochtime % roundto
    return datetime.datetime.fromtimestamp(dt).strftime(dt_format)


class MetricsProcessor(object):

    def __init__(self, name, pattern, roundto=900):

        self._name = name
        self._pattern = re.compile(pattern)
        self._roundto = roundto
        self._metrics = list()

    def add_event(self, fields):

        for k,v in fields.items():
            if self._pattern.search(k):
                if isinstance(v, int):
                    self._metrics.append({'datetime': dt_round(v, self._roundto), 'value': 1})
                else:
                    logger.error('Unknown value type: %s' % type(v))

    def process(self):

        self._metrics.sort(key=operator.itemgetter('datetime'))
        for dt, items in itertools.groupby(self._metrics, key=operator.itemgetter('datetime')):
            print dt, sum([i['value'] for i in items])
            # pass

    def metrics(self):

        return self._metrics
