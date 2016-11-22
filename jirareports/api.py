
import utils

from storage import Storage


jira = utils.import_module('jira', package='jirareports')

class JiraAPI(object):

    def __init__(self, host, username, password):

        self._host = host
        self._username = username
        self._password = password

        self._jira_server = jira.JIRA(self._host, basic_auth=(self._username, self._password))


    def search(self, JQL, maxResults=2000, expand="changelog"):
        ''' search issues by JQL and returns the list of issues
        '''
        for issue in self._jira_server.search_issues(JQL, maxResults=2000, expand="changelog"):
            yield self._handle_issue(issue)


    def _handle_issue(self, issue):
        ''' select only specific issue fields and returns them as dict
        '''
        details = {}
        details['issue'] = issue.key
        # details['assignee'] = "%s <%s>" % (issue.fields.assignee.displayName, issue.fields.assignee.name) if issue.fields.assignee else ""
        details['assignee'] = issue.fields.assignee.displayName if issue.fields.assignee else ""
        details['components'] = [component.name for component in issue.fields.components]
        details['created'] = issue.fields.created
        # details['creator'] = "%s <%s>" % (issue.fields.creator.displayName, issue.fields.creator.name) if issue.fields.creator else ""
        details['creator'] = issue.fields.creator.displayName if issue.fields.creator else ""
        # details['description'] = issue.fields.description
        details['duedate'] = issue.fields.duedate
        details['environment'] = issue.fields.environment
        details['fixVersions'] = [version.name for version in issue.fields.fixVersions]
        # details['issuelinks'] = [link for link in issue.fields.issuelinks]
        details['issuetype'] = issue.fields.issuetype.name
        details['labels'] = [label for label in issue.fields.labels]
        # details['lastViewed'] = issue.fields.lastViewed
        details['priority'] = issue.fields.priority.name
        # details['progress'] = issue.fields.progress.progress
        details['project'] = {"key": issue.fields.project.key, "name": issue.fields.project.name}
        # details['reporter'] = "%s <%s>" % (issue.fields.reporter.displayName, issue.fields.reporter.name) if issue.fields.reporter else ""
        details['reporter'] = issue.fields.reporter.displayName if issue.fields.reporter else ""
        details['resolution'] = issue.fields.resolution.name if issue.fields.resolution else ""
        details['resolutiondate'] = issue.fields.resolutiondate
        details['status'] = issue.fields.status.name
        details['subtasks'] = [t.key for t in issue.fields.subtasks]
        details['summary'] = issue.fields.summary
        details['timeestimate'] = issue.fields.timeestimate
        # details['timeoriginalestimate'] = issue.fields.timeoriginalestimate
        details['timespent'] = issue.fields.timespent
        details['updated'] = issue.fields.updated
        details['versions'] = [version.name for version in issue.fields.versions]
        # details['workratio'] = issue.fields.workratio
        details['changelog'] = self._changelog(issue)
        return details


    def _changelog(self, issue):
        ''' returns issue changelog
        '''
        changelog = []
        for history in issue.changelog.histories:
            for item in history.items:
                if item.field == 'assignee':
                    changelog.append({'date': history.created, 'field': item.field, 'from': item.fromString, 'to': item.toString})
                if item.field == 'status':
                    changelog.append({'date': history.created, 'field': item.field, 'from': item.fromString, 'to:': item.toString})
        return changelog


    def export(self, issue, storage_path):
        ''' export issue to storage

        where path - the path to the storage
        '''
        _storage = Storage(storage_path)
        _storage.put(issue.pull('issue'), issue)
