
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

from api import JiraAPI
from profile import Profile
from storage import Storage

def run():

    parser = argparse.ArgumentParser(prog=__title__)
    parser.add_argument('-v', '--version', action='version', version='v%s' % __version__)
    parser.add_argument('-p', '--profile', required=True,
            action='append', help='the path to the package profile, yaml file')
    parser.add_argument('-a', '--alias', help='the JQL alias in the profile')
    parser.add_argument('-d', '--dump', action='store_true', help='dump issues to file storage')
    parser.add_argument('-r', '--report', action='store_true', help='generate reports')
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
            process(profile_path, args.alias, **{'dump': args.dump, 'report': args.report})
    else:
        parser.print_help()


def process(profile_path, alias, **opts):

    _profile = Profile(profile_path)
    if not alias and 'jira.jqls.default' not in _profile.jql():
        logger.error('The alias is not specified')
        sys.exit(1)

    JQL = None
    if alias:
        JQL = _profile.jql(alias)
    if not JQL:
        raise RuntimeError('JQL is not specified')

    if 'dump' in opts and opts['dump']:
        logger.info('Dumping issues into the storage: %s' % opts['dump'])
        dump(JQL, _profile.hostname, _profile.username, _profile.password, _profile.storage)


def dump(JQL, hostname, username, password, storage_path):
    ''' dump issues to the file storage
    '''
    _storage = Storage(storage_path)
    _api = JiraAPI(hostname, username, password)

    for issue in _api.search(JQL):
        sys.stdout.write('.')
        _storage.put(issue['issue'], **issue)
