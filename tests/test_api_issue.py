
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
    u'customfield_01': 1000,
    u'customfield_02': 2000,
    u'customfield_03': 3000,
    u'customfield_04': 4000,
}

FIELDSMAP_SAMPLE = {
    u'customfield_01': u'field 01',
    u'customfield_02': u'field 02',
    u'customfield_03': u'field 03',
}

def test_api_issue_fields_create():

    issue = api.IssueFields(FIELDS_SAMPLE)
    assert isinstance(issue, api.IssueFields)


def test_api_issue_fields_create_incorrect_type():

    with pytest.raises(RuntimeError):
        issue = api.IssueFields([])


def test_api_issue_fields_rename_fields():

    issue_fields = api.IssueFields(FIELDS_SAMPLE)
    assert isinstance(issue_fields, api.IssueFields)

    assert set(issue_fields.fields().keys()) == set([
        u'assignee',
        u'customfield_01',
        u'customfield_02',
        u'customfield_03',
        u'customfield_04'
    ])
    issue_fields = issue_fields.rename(FIELDSMAP_SAMPLE)
    assert set(issue_fields.fields().keys()) == set([
        u'assignee',
        u'field 01',
        u'field 02',
        u'field 03',
        u'customfield_04'
    ])


def test_api_issue_fields_flatten():

    issue_fields = api.IssueFields(FIELDS_SAMPLE).flatten()
    assert isinstance(issue_fields, api.IssueFields)

    assert set(issue_fields.fields().keys()) == set([
        u'customfield_01',
        u'customfield_02',
        u'customfield_03',
        u'customfield_04',
        u'assignee.self',
        u'assignee.name',
        u'assignee.active',
        u'assignee.emailAddress',
        u'assignee.displayName',
        u'assignee.avatarUrls.16x16',
        u'assignee.avatarUrls.24x24',
        u'assignee.avatarUrls.32x32',
        u'assignee.avatarUrls.48x48',
    ])


def test_api_issue_fields_filter():

    issue_fields = api.IssueFields(FIELDS_SAMPLE).flatten().filter([
        r'^customfield_\d+',
        r'^assignee\.avatarUrls',
    ])
    assert isinstance(issue_fields, api.IssueFields)
    print issue_fields.fields()
    assert set(issue_fields.fields().keys()) == set([
        u'assignee.displayName',
        u'assignee.name',
        u'assignee.emailAddress',
        u'assignee.active',
        u'assignee.self',
    ])
