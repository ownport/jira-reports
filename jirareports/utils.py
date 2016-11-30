
import re
import importlib

def import_module(name, package=None):
    ''' returns imported module (vendored)
    '''
    package_prefix = ''
    if package and package_exists(package):
        package_prefix = '%s.' % package

    params = (package_prefix, name)
    return importlib.import_module('%svendor.%s' % params)


def package_exists(name):
    ''' check if package exists and can be imported
    '''
    try:
        __import__(name)
    except ImportError:
        return False
    else:
        return True


def dict2flat(root_name, source, removeEmptyFields=False):
    ''' returns a simplified "flat" form of the complex hierarchical dictionary
    '''

    def is_simple_elements(source):
        ''' check if the source contains simple element types,
        not lists, tuples, dicts
        '''
        for i in source:
            if isinstance(i, (list, tuple, dict)):
                return False
        return True

    flat_dict = {}
    if isinstance(source, (list, tuple)):
        if not is_simple_elements(source):
            for i,e in enumerate(source):
                new_root_name = "%s[%d]" % (root_name,i)
                for k,v in dict2flat(new_root_name,e).items():
                    flat_dict[k] = v
        else:
            flat_dict[root_name] = source
    elif isinstance(source, dict):
        for k,v in source.items():
            if root_name:
                new_root_name = "%s.%s" % (root_name, k)
            else:
                new_root_name = "%s" % k
            for kk, vv in dict2flat(new_root_name,v).items():
                flat_dict[kk] = vv
    else:
        if source is not None:
            flat_dict[root_name] = source
    return flat_dict


def optimize_timeintervals(intervals):
    ''' returns duration and time intervals for specific values

    if the duration is not equal 0, time intervals optimization was failed

    for better understanding the logic below please see
    - tests/test_api_issue_timeline.py#test_api_issue_timeline_experiment_01
    '''
    big_ts1, big_ts2, big_val1, big_val2 = intervals.pop(0)
    duration = big_ts2 - big_ts1

    if len(intervals) == 0:
        return 0, (big_ts1, big_ts2, big_val2)

    result = list()
    sm_ts1, sm_ts2, sm_val1, sm_val2 = (0, 0, None, None)
    while len(intervals) > 0:
        sm_ts1, sm_ts2, sm_val1, sm_val2 = intervals.pop(0)
        if sm_ts1 == big_ts1 and sm_ts2 <= big_ts2+1:
            big_ts1 = sm_ts2
            result.append([sm_ts1, sm_ts2, sm_val1])
            duration = duration - (sm_ts2 - sm_ts1)

    if big_ts1 == sm_ts2 and big_ts2 > sm_ts2:
        result.append([big_ts1, big_ts2, big_val2])
        duration = duration - (big_ts2 - big_ts1)

    return duration, result
