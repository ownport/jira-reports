
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

from api import JiraAPI
from api import IssueFields
from api import IssueChangelog
from api import IssueTimeline

from profile import Profile
from storage import Storage

from pprint import pprint


def run():

    parser = argparse.ArgumentParser(prog=__title__)
    parser.add_argument('-v', '--version', action='version', version='v%s' % __version__)
    parser.add_argument('-p', '--profile', required=True,
            action='append', help='the path to the package profile, yaml file')
    parser.add_argument('-a', '--alias', help='the JQL alias in the profile')
    parser.add_argument('-d', '--dump', action='store_true', help='dump issues to file storage')
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

    if args.profile:
        for profile_path in args.profile:
            if not os.path.exists(profile_path):
                logger.error('The path to profile does not exist, %s' % profile_path)
                sys.exit(1)
            process(profile_path, args.alias, **{'dump': args.dump, 'reports': args.reports})
    else:
        parser.print_help()


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

        dump(JQL, _profile.hostname, _profile.username, _profile.password, _profile.storage)
        sys.exit(0)

    if 'reports' in opts and opts['reports']:
        logger.info('Collecting data for reports')
        reports(_profile.storage, _profile.ignored_fields, _profile.changelog_mapping)
        logger.info('Data collection for reports was completed')
        sys.exit(0)

    logger.info('Dumping issues into the storage')


def dump(JQL, hostname, username, password, storage_path):
    ''' dump issues to the file storage
    '''
    logger.info('Storage path: %s' % storage_path)
    _api = JiraAPI(hostname, username, password)

    # fields
    _storage = Storage(name='fields', path=storage_path)
    for field in _api.fields():
        _storage.put(field['id'], field)
    _storage.close()

    # issues
    _storage = Storage(name='issues', path=storage_path)
    for n, issue in enumerate(_api.search(JQL)):
        _storage.put(issue['key'], issue)
    logger.info('Issues dump was completed, total issues: %s' % (n+1))
    _storage.close()


def reports(storage_path, ignored_fields, changelog_mapping):
    ''' prepare data for reporting
    '''
    logger.info('Update issue events')

    logger.info('Collecting field list')
    fieldsmap = {v['id']:v['name'] for k,v in Storage(name='fields', path=storage_path).get()}

    for _key, issue in Storage(name='issues', path=storage_path).get():

        issue_fields = IssueFields(issue['fields']).rename(fieldsmap)
        issue_fields = issue_fields.flatten().filter(ignored_fields).simplify()
        # pprint(issue_fields.fields())
        print "-------------"

        changelog = IssueChangelog(issue['changelog']['histories']).simplify().sort()
        # pprint([l for l in changelog])
        # print "============="

        timeline = IssueTimeline(_key, issue_fields, changelog, changelog_mapping).timeline()
        pprint(timeline.fields())
        print "============="

        break
    #     print
    #
    #     changelog = Changelog(issue['changelog']['histories'])
