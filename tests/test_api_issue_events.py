
import pytest

from jirareports import api

FIELDS_SAMPLE = {
    u'assignee': {
        u'active': True,
        u'avatarUrls': {
            u'24x24': u'https://avatar.example.com/avatar/1?d=mm&s=24',
            u'16x16': u'https://avatar.example.com/avatar/1?d=mm&s=16',
            u'48x48': u'https://avatar.example.com/avatar/1?d=mm&s=48',
            u'32x32': u'https://avatar.example.com/avatar/1?d=mm&s=32'
        },
        u'displayName': u'user1',
        u'emailAddress': u'user1@mail.example.com',
        u'name': u'user1',
        u'self': u'https://jira.example.com/rest/api/2/user?username=user1'
    },
    u'created': u'2015-12-01T19:09:59.000+0000',
    u'customfield_01': 1000,
    u'customfield_02': 2000,
    u'customfield_03': 3000,
    u'customfield_04': 4000,
    u'updated': u'2016-09-12T14:31:13.000+0000',
    u'status': {
        u'name': 'Closed',
    }
}

CHANGELOG_SAMPLE = [
    {
        u'items': [
            {
                u'field': u'description', u'fieldtype': u'jira',
                u'from': None, u'fromString': u'test-from',
                u'to': None, u'toString': u'test-to'
            }
        ],
        u'author': {
            u'displayName': u'user1',
            u'name': u'user1',
            u'self': u'https://jira.example.com/rest/api/2/user?username=user1',
            u'avatarUrls': {
                u'24x24': u'https://avatar.example.com/avatar/1?d=mm&s=24',
                u'16x16': u'https://avatar.example.com/avatar/1?d=mm&s=16',
                u'48x48': u'https://avatar.example.com/avatar/1?d=mm&s=48',
                u'32x32': u'https://avatar.example.com/avatar/1?d=mm&s=32'
            },
            u'emailAddress': u'user1@mail.example.com',
            u'active': True
        },
        u'id': u'1',
        u'created': u'2016-09-12T11:34:04.000+0000'
    }, {
        u'items': [
            {
                u'field': u'assignee', u'fieldtype': u'jira',
                u'from': u'user1', u'fromString': u'user1',
                u'to': u'user2', u'toString': u'user2'
            }
        ],
        u'author': {
            u'displayName': u'user2',
            u'name': u'user2',
            u'self': u'https://jira.example.com/rest/api/2/user?username=user2',
            u'avatarUrls': {
                u'24x24': u'https://avatar.example.com/avatar/2?d=mm&s=24',
                u'16x16': u'https://avatar.example.com/avatar/2?d=mm&s=16',
                u'48x48': u'https://avatar.example.com/avatar/2?d=mm&s=48',
                u'32x32': u'https://avatar.example.com/avatar/2?d=mm&s=32'
            },
            u'emailAddress': u'user2@mail.example.com',
            u'active': True
        },
        u'id': u'2',
        u'created': u'2016-09-12T11:52:50.000+0000'
    }, {
        u'items': [
            {
                u'field': u'status', u'fieldtype': u'jira',
                u'from': u'1',  u'fromString': u'Open',
                u'to': u'3', u'toString': u'In Progress',
            }
        ],
        u'author': {
            u'displayName': u'user3',
            u'name': u'user3',
            u'self': u'https://jira.example.com/rest/api/2/user?username=user3',
            u'avatarUrls': {
                u'24x24': u'https://avatar.example.com/avatar/3?d=mm&s=24',
                u'16x16': u'https://avatar.example.com/avatar/3?d=mm&s=16',
                u'48x48': u'https://avatar.example.com/avatar/3?d=mm&s=48',
                u'32x32': u'https://avatar.example.com/avatar/3?d=mm&s=32'
            },
            u'emailAddress': u'user3@mail.example.com',
            u'active': True
        },
        u'id': u'3',
        u'created': u'2016-09-12T14:30:13.000+0000'
    }
]

CHANGELOG_MAPPING_SAMPLE = {
    u'assignee': u'assignee.name',
    u'status': u'status.name',
}

FIELDS_SAMPLE_FOR_OPTIMIZATION = {
    u'status': [
        (1449084416, None, None),
        (1473161751, None, u'Closed'),
        (1449158492, u'Open', u'Resolved'),
        (1449159411, u'Resolved', u'Closed'),
        (1453240059, u'Closed', u'Resolved'),
        (1473161751, u'Resolved', u'Closed')
    ],
}

def test_api_issue_events_create():

    events = api.IssueEvents(
        api.IssueFields(FIELDS_SAMPLE),
        api.IssueChangelog(CHANGELOG_SAMPLE),
        CHANGELOG_MAPPING_SAMPLE
    )
    assert isinstance(events, api.IssueEvents)


def test_api_issue_events_events():

    events = api.IssueEvents(
        api.IssueFields(FIELDS_SAMPLE),
        api.IssueChangelog(CHANGELOG_SAMPLE),
        CHANGELOG_MAPPING_SAMPLE
    )

def test_api_issue_checkpoints_create():

    issue_checkpoints = api.IssueCheckpoints(
        '01',
        api.IssueFields(FIELDS_SAMPLE),
        api.IssueChangelog(CHANGELOG_SAMPLE),
        CHANGELOG_MAPPING_SAMPLE
    )
    assert isinstance(issue_checkpoints, api.IssueCheckpoints)


def test_api_issue_checkpoints_checkpoints():

    fields = api.IssueFields(FIELDS_SAMPLE).flatten().lower_keys().simplify()
    changelog = api.IssueChangelog(CHANGELOG_SAMPLE).simplify().sort()

    checkpoints = api.IssueCheckpoints(
        '01', fields, changelog, CHANGELOG_MAPPING_SAMPLE
    ).checkpoints()
    assert isinstance(checkpoints, api.IssueFields)

    fields_with_checkpoints = checkpoints.fields()
    assert set(fields_with_checkpoints.keys()) == set([
        u'assignee.active',
        u'assignee.avatarurls.16x16',
        u'assignee.avatarurls.24x24',
        u'assignee.avatarurls.32x32',
        u'assignee.avatarurls.48x48',
        u'assignee.displayname',
        u'assignee.emailaddress',
        u'assignee.name',
        u'assignee.self',
        u'created',
        u'customfield_01',
        u'customfield_02',
        u'customfield_03',
        u'customfield_04',
        u'status.name',
        u'updated',
    ])
    assert fields_with_checkpoints[u'created'] == 1448996999
    assert fields_with_checkpoints[u'updated'] == 1473690673
