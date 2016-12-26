
import os
import utils

yaml = utils.import_module('yaml', package='jirareports')

class Profile(object):

    def __init__(self, path):

        self._path = path
        self._profile = None
        with open(path, 'r') as _profile:
            self._profile = yaml.load(_profile)

    @property
    def hostname(self):
        ''' returns hostname
        '''
        return self._profile.get('jira.hostname', None)

    @property
    def username(self):
        ''' returns username
        '''
        return self._profile.get('jira.username', None)

    @property
    def password(self):
        ''' returns password
        '''
        return self._profile.get('jira.password', None)

    @property
    def storage(self):
        ''' returns storage path
        '''
        return self._profile.get('jira.issues.storage', None)


    def jql(self, alias=None):
        ''' returns JQL by alias
        if no aliases are specified, returns the list of aliases in the profile
        '''
        jqls = self._profile.get('jira.jqls', None)
        if not isinstance(jqls, dict):
            raise RuntimeError('The type of jql shall be dict, %s' % type(jqls))

        if not alias:
            return jqls.keys()
        elif alias not in jqls:
            raise RuntimeError('The alias "%s" is absent in the profile: %s' % (alias, self._path))
        else:
            return jqls.get(alias, None)

    @property
    def ignored_fields(self):
        ''' returns fields which shall be ignored
        '''
        return self._profile.get('jira.reports.preprocessing.fields.ignore', None)

    @property
    def changelog_mapping(self):
        ''' returns changelog mapping for merging issue fields with changelog
        '''
        return self._profile.get('jira.reports.preprocessing.changelog.mapping', None)

    @property
    def metrics(self):
        ''' returns the list of metrics
        '''
        return self._profile.get('jira.metrics', None)
