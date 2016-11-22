
import os
import sys
import argparse

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
    parser.add_argument('-d', '--dump', action='store_false', help='dump issues to file storages')
    parser.add_argument('-r', '--report', action='store_false', help='generate reports')
    args = parser.parse_args()

    if args.profile:
        for profile_path in args.profile:
            if not os.path.exists(profile_path):
                print >> sys.stderr, '[ERROR] The path to profile does not exist, %s' % profile
                sys.exit(1)
            process(profile_path, args.alias, **{'dump': args.dump, 'report': args.report})
    else:
        parser.print_help()


def process(profile_path, alias, **opts):

    _profile = Profile(profile_path)
    if not alias and 'jira.jqls.default' not in _profile.jql():
        raise RuntimeError('The alias is not specified')

    JQL = None
    if alias:
        JQL = _profile.jql(alias)
    if not JQL:
        raise RuntimeError('JQL is not specified')

    if 'dump' in opts and opts['dump']:
        print >> sys.stderr, '[INFO] Dumping issues into the storage: %s' % opts['dump']
        dump(JQL, _profile.hostname, _profile.username, _profile.password, _profile.storage)


def dump(JQL, hostname, username, password, storage_path):
    ''' dump issues to the file storage
    '''
    _storage = Storage(storage_path)
    _api = JiraAPI(hostname, username, password)

    for issue in _api.search(JQL):
        sys.stdout.write('.')
        _storage.put(issue['issue'], **issue)
    print
    
