
import utils

sqlitedict = utils.import_module('sqlitedict', package='jirareports')


class Storage(object):

    def __init__(self, name, path):

        if not name:
            raise RuntimeError('Storage name does not specified, %s' % name)
        self._storage = sqlitedict.SqliteDict(path, tablename=name, autocommit=True)


    def put(self, issue_id, details):
        ''' put issue into storage
        '''
        self._storage[issue_id] = details


    def get(self, issue_id=None):
        ''' get issue details by the issue id
        '''
        if not issue_id:
            return self._storage.items()
        else:
            return self._storage[issue_id]

    def close(self):
        ''' close storage
        '''
        self._storage.close()
