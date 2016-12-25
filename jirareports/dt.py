
# Supported functions
#
# - now()      return the time since the epoch
# - minute(n)  return n x minute(s) in seconds, n = 1 is default
# - hour(n)    return n x hour(s) in seconds, n = 1 is default
# - day(n)     return n x day(s) in seconds, n = 1 is default

import sys
import time
import calendar
import datetime


NOW = calendar.timegm(time.localtime())

def epoch2dt(epochtime):
    ''' returns epoch time in %Y-%m-%d %H:%M:%S format
    '''
    dt_format = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.fromtimestamp(epochtime).strftime(dt_format)


def roundto(epochtime, roundto):
    ''' return rounded epoch time to 'roundto' value
    '''
    return epochtime - epochtime % roundto

def roundto_range(dt_start, dt_end, roundto):
    ''' return rounded epoch time to 'roundto' value and format to the next formats:
    '''
    result = list()
    dt_point = dt_start - dt_start % roundto
    result.append(dt_point)
    while dt_point + roundto <= dt_end:
        dt_point += roundto
        result.append(dt_point)
    return result


def dt_format(epochtime, roundto):
    ''' return formatted epochtime in the next formats, according to roundto value:
    # - %Y-%m-%d %H:%M:%S -> roundto = 0
    # - %Y-%m-%d %H:%M -> roundto = 900
    # - %Y-%m-%d %H -> roundto = 3600
    # - %Y-%m-%d -> roundto = 86400
    '''
    dt_format = '%Y-%m-%d %H:%M:%S'
    if roundto >= 86400:
        dt_format = '%Y-%m-%d'
    elif roundto >= 3600:
        dt_format = '%Y-%m-%d %H'
    elif roundto >= 60:
        dt_format = '%Y-%m-%d %H:%M'
    return datetime.datetime.fromtimestamp(epochtime).strftime(dt_format)


def now():
    ''' return the time since the epoch
    '''
    return NOW

def minute(n=1):
    ''' return n x minute(s) in seconds
    '''
    return n * 60

def hour(n=1):
    ''' return n x hour(s) in seconds
    '''
    return n * minute(60)

def day(n=1):
    ''' return n x day(s) in seconds
    '''
    return n * hour(24)
