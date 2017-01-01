
import os
import sys
import argparse

import logging
# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logger = logging.getLogger(__name__)

from __init__ import __title__
from __init__ import __version__

import utils

from profile import Profile
from storage import Storage

from api import JiraAPI
from api import IssueFields
from api import IssueChangelog
from api import IssueTimeline
from api import IssueCheckpoints

import dt
import metrics

from pprint import pprint


def run():

    parser = argparse.ArgumentParser(prog=__title__)
    parser.add_argument('-v', '--version', action='version', version='v%s' % __version__)
    parser.add_argument('-p', '--profile', required=True,
            action='append', help='the path to the package profile, yaml file')
    parser.add_argument('-a', '--alias', help='the JQL alias in the profile')
    parser.add_argument('-d', '--dump', action='store_true', help='dump issues to file storage')
    parser.add_argument('-u', '--update', action='store_true', help='update checkpoints')
    parser.add_argument('-r', '--reports', action='store_true', help='generate reports')
    parser.add_argument('-l', '--logging', type=str,
            help='logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    args = parser.parse_args()

    log_level = logging.ERROR
    if args.logging:
        log_level = getattr(logging, args.logging.upper(), None)
        if not isinstance(log_level, int):
            logger.warning('Invalid log level: %s' % log_level)
            logger.info('Default log level: ERROR')

    logging.basicConfig(level=log_level,
                        handler=NullHandler(),
                        format="%(asctime)s (%(name)s) [%(levelname)s] %(message)s"
    )

    try:
        if args.profile:
            for profile_path in args.profile:
                if not os.path.exists(profile_path):
                    logger.error('The path to profile does not exist, %s' % profile_path)
                    sys.exit(1)
                process(profile_path, args.alias, **{
                            'dump': args.dump,
                            'update': args.update,
                            'reports': args.reports
                })
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("Interrupted by user")
        sys.exit(1)

def process(profile_path, alias, **opts):

    _profile = Profile(profile_path)

    if 'dump' in opts and opts['dump']:
        logger.info('Dumping issues into the storage')

        if not alias and 'jira.jqls.default' not in _profile.jql():
            logger.error('The alias is not specified')
            sys.exit(1)

        JQL = None
        if alias:
            JQL = _profile.jql(alias)
        if not JQL:
            logger.error('JQL is not specified in profile "%s" for alias "%s"' % (profile_path, alias))
            sys.exit(1)

        dump(JQL, _profile)

    elif 'update' in opts and opts['update']:
        logger.info('Updating checkpoints for reports')
        update(_profile)
        logger.info('Updating checkpoints for reports was completed')

    elif 'reports' in opts and opts['reports']:
        logger.info('Collecting data for reports')
        reports(_profile)
        logger.info('Data collection for reports was completed')



def dump(JQL, profile):
    ''' dump issues to the file storage
    '''
    logger.info('Storage path: %s' % profile.storage)
    _api = JiraAPI(profile.hostname, profile.username, profile.password)

    # fields
    logger.info('Updating field list')
    _storage = Storage(name='fields', path=profile.storage)
    for field in _api.fields():
        _storage.put(field['id'], field)
    _storage.close()

    # issues
    _storage = Storage(name='issues', path=profile.storage)
    for n, issue in enumerate(_api.search(JQL)):
        _storage.put(issue['key'], issue)
    logger.info('Issues dump was completed, total issues: %s' % (n+1))
    _storage.close()


def update(profile):

    logger.info('Preparing fields map')
    # fieldsmap
    # keys and values in the fields map shall be in lower case
    fieldsmap = {v['id'].lower():v['name'].lower() for k,v in Storage(name='fields', path=profile.storage).get()}

    logger.info('Updating changelog')
    intervals = Storage(name='intervals', path=profile.storage)
    for _key, issue in Storage(name='issues', path=profile.storage).get():
        issue_fields = IssueFields(issue['fields']).rename(fieldsmap)

        checkpoints = IssueCheckpoints(
                            _key,
                            issue_fields.flatten().lower_keys().filter(profile.ignored_fields).simplify(),
                            IssueChangelog(issue['changelog']['histories']).simplify().sort(),
                            profile.changelog_mapping
        ).checkpoints()
        intervals.put(_key, dict([ (k, utils.create_timeintervals(v) if isinstance(v, list) else v)
                                        for k,v in checkpoints.fields().items()]))
    intervals.close()
    logger.info('Changelog update was completed')



def reports(profile):
    ''' prepare data for reporting
    '''
    logger.info('Collecting metrics')

    # metrics processors
    processors = metrics.get_metric_processors(profile.metrics)

    for k,v in Storage(name='intervals', path=profile.storage).get():
        v['issue_id'] = k
        for name in processors:
            processors[name].add_event(v)

    for pname, proc in processors.items():
        filtered_metrics = proc.metrics().filter(dt.now()-3*dt.day(30), dt.now()).conv(proc.roundto)
        logger.info('%d points for metric: %s' % (len(filtered_metrics.items()), pname))
        open(os.path.join(proc.path, '%s.json' % pname), 'w').write(filtered_metrics.json())
