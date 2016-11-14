
import pytest
from jirareports.profile import Profile

PROFILE='''
jira.hostname: http://jira.example.com
jira.username: username
jira.password: password

jira.jqls:
  jql1: project=Test1
  jql2: project=Test2
  jql3: project=Test3
'''

PROFILE_EMPTY_JQL_LIST='''
jira.jqls:
'''


def create_profile_file(handler, profile_name):

    _file = handler.join('profile.yml')
    _file_path = str(_file)
    _file.write(profile_name)
    return _file_path


def test_profile_create(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    assert isinstance(_profile, Profile)


def test_profile_hostname(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    assert _profile.hostname == 'http://jira.example.com'


def test_profile_username(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    assert _profile.username == 'username'


def test_profile_password(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    assert _profile.password == 'password'


def test_profile_jqls_list(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    assert set(_profile.jql()) == set(['jql1', 'jql2', 'jql3'])


def test_profile_jql_alias(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    assert _profile.jql('jql1') == 'project=Test1'


def test_profile_jql_absent_alias(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE))
    with pytest.raises(RuntimeError):
        assert _profile.jql('jqlX') == None


def test_profile_jqls_empty_list(tmpdir):

    _profile = Profile(create_profile_file(tmpdir, PROFILE_EMPTY_JQL_LIST))
    with pytest.raises(RuntimeError):
        assert _profile.jql() == []
