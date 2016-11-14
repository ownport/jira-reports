
from sqlitedict import SqliteDict


class Storage(object):

    def __init__(self, path):

        self._storage = SqliteDict(path)


    def put(self, issue_id, **details):
        ''' put issue into storage
        '''
        self._storage[issue_id] = details


    def get(self, issue_id):
        ''' get issue details by the issue id
        '''
        return self._storage[issue_id]
