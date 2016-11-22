
import utils

sqlitedict = utils.import_module('sqlitedict', package='jirareports')


class Storage(object):

    def __init__(self, path):

        self._storage = sqlitedict.SqliteDict(path, autocommit=True)


    def put(self, issue_id, **details):
        ''' put issue into storage
        '''
        self._storage[issue_id] = details


    def get(self, issue_id):
        ''' get issue details by the issue id
        '''
        return self._storage[issue_id]
