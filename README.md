# jira-reports

[![Build Status](https://travis-ci.org/ownport/jira-reports.svg?branch=master)](https://travis-ci.org/ownport/jira-reports)
[![codecov](https://codecov.io/gh/ownport/jira-reports/branch/master/graph/badge.svg)](https://codecov.io/gh/ownport/jira-reports)

Jira reports tools


## Storage formats

- fields
- issues
- intervals

## Configuration file (profile)

The profile divided in several sections:

- Jira account details
- The list of JQLs and their aliases
- Storage details
- Preprocessing details: fields ignore list, fields mappings
- Metrics details

### Jira account details

```yaml
jira.hostname: https://jira.example.com/
jira.username: test-username
jira.password: test-password
```

### The list of JQLs and their aliases

```yaml
jira.jqls:
  all-issues: project in (TestProject1, TestProject2)
  all-issues-created-during-last-month: project in (TestProject1, TestProject2) and created >= startOfMonth(0)
```

### Storage details

```yaml
jira.issues.storage: /home/dev/jira-reports/issues.sqlite
```

### Preprocessing details: fields ignore list, fields mappings

the list of regular expressions for ignoring fields before reporting

```yaml
jira.reports.preprocessing.fields.ignore:
- "^watchers"
- "^support group"
- "\\.avatarurls\\."
- "\\.iconurl$"
- "description$"
- "fromstring$"
- "tostring$"
- "\\.emailaddress$"
```

changelog fields mapping
```yaml
jira.reports.preprocessing.changelog.mapping:
  status: status.name
  assignee: assignee.displayname
```

### Metrics

The list of report's metrics

```yaml
jira.metrics:

- name: created-issues-per-day
  path: /home/dev/jira-reports/html/data/
  type: SimpleMetric
  pattern: '^created$'
  roundto: 86400
```

## Metrics

- SimpleMetric
- EdgeMetric
- RangeMetric
- MultiPatternMetric
