[![Build Status](https://travis-ci.com/mwiens91/jira-ticket-migrate.svg?branch=master)](https://travis-ci.com/mwiens91/jira-ticket-migrate)
[![codecov](https://codecov.io/gh/mwiens91/jira-ticket-migrate/branch/master/graph/badge.svg)](https://codecov.io/gh/mwiens91/jira-ticket-migrate)
[![PyPI](https://img.shields.io/pypi/v/jira-ticket-migrate.svg)](https://pypi.org/project/jira-ticket-migrate/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jira-ticket-migrate.svg)](https://pypi.org/project/jira-ticket-migrate/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# jira-ticket-migrate

This is a program to help migrate tickets between Jira servers. *If* you
have the appropriate privileges, there are better ways of doing this! If
you don't, all you have available are messy solutions (including this).

So what's this, then? This migrates tickets belonging to projects from
one Jira server to Jira another server. If the project is fresh on the
destination server, then ticket numbers will be preserved.

To see what's done, a set of before and after pictures tells the best
story:

**Source ticket**

[![source ticket](https://i.imgur.com/UcbywFd.png)](https://i.imgur.com/KkGAD7b.png)

**Migrated ticket**

[![migrated ticket](https://i.imgur.com/ddMvuBd.png)](https://i.imgur.com/qIBUhQv.png)

Notice that the following are preserved:

+ title
+ description
+ priority
+ status
+ resolution

And possibly add the ticket number to that list (see above paragraph).
Everything else is not preserved.

Note that this program assumes that you're migrating to a new-ish Jira
(2018-ish), since there are some key differences between old and new
Jiras.

## Installation

Using pip,

```
pip install jira-ticket-migrate
```

Alternatively, you can run jira-ticket-migrate directly from source
using the script
[`run_jira_ticket_migrate.py`](run_jira_ticket_migrate.py).

## Usage

Copy the example config file
[`config.yaml.example`](config.yaml.example) to `config.yaml`

```
cp config.yaml.example config.yaml
```

and fill it in.

Then run with

```
jira-ticket-migrate
```

You can specify a config file explicitly with the `-c` option:

```
jira-ticket-migrate /path/to/config.yaml
```

Otherwise it will look for it at the root of the repository.
