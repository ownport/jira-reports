
import re
import json
import logging


from time import time
from operator import itemgetter

logger = logging.getLogger(__name__)

import dt
import utils
from storage import Storage

jira = utils.import_module('jira', package='jirareports')


class JiraAPI(object):

    def __init__(self, host, username, password):

        self._host = host
        self._username = username
        self._password = password

        self._jira_server = jira.JIRA(self._host, basic_auth=(self._username, self._password))

    def fields(self):
        ''' return Jira fields
        '''
        _fields = self._jira_server.fields()
        logger.info('Total fields: %s' % len(_fields))
        for field in _fields:
            yield field


    def search(self, JQL, maxResults=2000, expand="changelog"):
        ''' search issues by JQL and returns the list of issues
        '''
        result = self._jira_server.search_issues(JQL, maxResults=2000, expand="changelog", json_result=True)

        logger.info('Search results, JQL: %s' % JQL)
        logger.info('Search results, founded issues (total): %s' % result['total'])
        logger.info('Search results, max results: %s/%s' % (result['maxResults'], maxResults))
        logger.info('Search results, start at: %s' % result['startAt'])

        for issue in result['issues']:
            yield issue

    def export(self, issue, storage_path):
        ''' export issue to storage

        where path - the path to the storage
        '''
        _storage = Storage(storage_path)
        _storage.put(issue.pull('issue'), issue)


class IssueChangelog(object):

    def __init__(self, data):

        if not isinstance(data, list):
            raise RuntimeError('Changelog shall be list type, %s' % type(data))
        self._log = data


    def simplify(self):
        ''' remove extra fields
        '''
        result = list()
        for log in self._log:

            # remove extra fields
            log.pop(u'id', None)

            # simplify 'author' field
            author = log.pop('author', None)
            if author:
                author = author[u'displayName']
            log[u'author'] = author

            # simplify 'created' field
            try:
                log[u'created'] = dt.to_epoch(log[u'created'])
            except:
                pass

            # simplify 'items' fields
            for i, item in enumerate(log[u'items']):
                # removing 'from', 'to', 'fieldtype'
                log[u'items'][i].pop('from', None)
                log[u'items'][i].pop('to', None)
                log[u'items'][i].pop('fieldtype', None)
                # make field name in lower case
                log[u'items'][i]['field'] = log[u'items'][i]['field'].lower()
            result.append(log)
        return IssueChangelog(result)

    def sort(self):

        return IssueChangelog(sorted(self._log, key=itemgetter('created')))

    def dates(self):

        return [i[u'created'] for i in self._log]

    def logs(self):

        for log in self._log:
            yield log

    def __str__(self):

        return json.dumps(self._log)

    def __len__(self):

        return len(self._log)


class IssueFields(object):

    def __init__(self, fields):

        if not isinstance(fields, dict):
            raise RuntimeError('Fields shall be dict type, %s' % type(fields))
        self._fields = fields


    def flatten(self):

        return IssueFields(utils.dict2flat(None, self._fields))


    def fields(self):
        ''' return issue fields
        '''
        return self._fields


    def copy(self):

        return IssueFields(self._fields)


    def rename(self, fieldsmap):
        ''' rename issue fields according to fieldsmap
        '''
        return IssueFields({fieldsmap.get(k, k).lower(): v for k,v in self._fields.items()})


    def filter(self, rules):
        ''' fields filter
        '''
        result = dict()
        for k,v in self._fields.items():
            matched = False
            for r in rules:
                if re.search(r, k):
                    matched = True
                    break
            if not matched:
                result[k] = v
        return IssueFields(result)

    def simplify(self):
        ''' simplify issue fields
        '''
        result = dict()
        for k,v in self._fields.items():
            k = k.lower()
            # check if the field contains known datatime formats
            if isinstance(v, (str, unicode)) and re.search(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}\.\d+', v):
                result[k] = dt.to_epoch(v)
            else:
                result[k] = v
        return IssueFields(result)

    def lower_keys(self):
        ''' make lower keys for fields map
        '''
        return IssueFields(dict([(k.lower(), v) for k,v in self._fields.items()]))


class IssueEvents(object):

    def __init__(self, fields, changelog, mapping):

        self._fields = fields
        self._changelog = changelog
        self._mapping = mapping


    def with_intervals(self, fieldname, fieldvalue=None):
        ''' return time intervals for specified field name

        Optional, if fieldvalue parameter is specified, returns time intervals
        for specified name and value
        '''
        for k, v in self._fields.items():
            print k,v


class IssueCheckpoints(object):

    def __init__(self, issue_id, fields, changelog, mapping):

        self._issue_id = issue_id
        self._fields = fields
        self._changelog = changelog
        self._mapping = mapping

    def checkpoints(self):

        result = dict()

        issue_fields = self._fields.fields()

        current_time = int(time())
        created = issue_fields.get(u'created')
        updated = issue_fields.get(u'updated')
        status = issue_fields.get(u'status.name')

        # check fields
        for k,v in issue_fields.items():
            if k.lower() == 'created' or k.lower() == 'updated':
                result[k] = v
                continue

            if status.lower() == 'closed':
                result[k] = [(created, None, None), (updated, None, v), (current_time, v, None)]
            else:
                result[k] = [(created, None, None), (current_time, v, None)]

        # check changelogs
        for log in self._changelog.logs():
            for item in log['items']:
                fieldname = self._mapping.get(item['field'], item['field'])
                if fieldname in result:
                    result[fieldname].append((log['created'], item['fromString'], item['toString']))
                else:
                    logger.debug('Cannot find the changelog field in the issues fields, %s' % fieldname)

        return IssueFields(result)



#
#   Warning! all keys for fields and changelogs shall be in lower case
#
class IssueTimeline(object):

    def __init__(self, issue_id, fields, changelog, mapping):

        self._issue_id = issue_id
        self._fields = fields
        self._changelog = changelog
        self._mapping = mapping
        self._timeline = list()


    def timeline(self):

        result = dict()

        issue_fields = self._fields.fields()

        created = issue_fields.get(u'created')
        updated = issue_fields.get(u'updated')
        status = issue_fields.get(u'status.name')
        current_time = int(time())

        for k,v in issue_fields.items():
            if k.lower() == 'created' or k.lower() == 'updated':
                result[k] = v
                continue

            if status.lower() == 'closed':
                result[k] = [(created, updated, None, v)]
            else:
                result[k] = [(created, current_time, None, v)]


        for log in self._changelog.logs():
            for item in log['items']:
                fieldname = self._mapping.get(item['field'], item['field'])
                if fieldname in result:
                    result[fieldname].append((None, log['created'], item['fromString'], item['toString']))
                else:
                    logger.warning('Cannot find the changelog field in the issues fields, %s' % fieldname)

        result = self._calc_timeintervals(result)
        return IssueFields(result)

    def _calc_timeintervals(self, fields):

        result = dict()
        for fieldname, events in fields.items():
            if isinstance(events, list):
                if len(events) == 1:
                    result[fieldname] = events
                    continue

                dt_min = dt_max = None
                new_events = list()

                for event in events:
                    event = list(event)
                    if not dt_min or not dt_max:
                        dt_min = event[0]
                        dt_max = event[1]
                        new_events.append(event)
                        continue

                    if event[1] < dt_max:
                        event[0] = dt_min
                        dt_max = event[1]
                        new_events.append(event)
                        continue

                    if event[1] > dt_max:
                        event[0] = dt_max
                        dt_min = event[0]
                        dt_max = event[1]
                        new_events.append(event)
                        continue
                result[fieldname] = new_events
            else:
                result[fieldname] = events

        for fieldname, events in result.items():
            if isinstance(events, list):
                duration, new_events = utils.optimize_timeintervals(list(events))
                if duration in [0, -1]:
                    result[fieldname] = new_events
                else:
                    raise RuntimeError({
                        'fieldname': fieldname,
                        'duration': duration,
                        'events.before': events,
                        'events.after': new_events
                    })
                    # retult[fieldname] = events
            else:
                result[fieldname] = events

        return result
