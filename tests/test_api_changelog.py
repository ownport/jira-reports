
import json
import pytest

from jirareports import api

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


def test_api_changelog_create():

    changelog = api.IssueChangelog(CHANGELOG_SAMPLE)
    assert isinstance(changelog, api.IssueChangelog)
    assert len(changelog) == 3


def test_api_changelog_create_incorrect_type():

    with pytest.raises(RuntimeError):
        changelog = api.IssueChangelog({})


def test_api_changelog_dates():

    changelog = api.IssueChangelog(CHANGELOG_SAMPLE)
    assert changelog.dates() == [
        '2016-09-12T11:34:04.000+0000',
        '2016-09-12T11:52:50.000+0000',
        '2016-09-12T14:30:13.000+0000',
    ]


def test_api_changelog_simplify():

    simplified_changelog = api.IssueChangelog(CHANGELOG_SAMPLE).simplify()
    for l in simplified_changelog.logs():
        assert l[u'created'] in [1473680044, 1473681170, 1473690613]
        assert l[u'author'] in ['user1', 'user2', 'user3']
        assert set(
                            [i[u'field'] for i in l[u'items']]
                ).issubset(
                            set([u'description', u'status', 'assignee'])
                )
