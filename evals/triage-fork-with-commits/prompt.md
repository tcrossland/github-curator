---
description: A fork with commits beyond its parent is never clear, even when none of them carry the user's login.
tags: [triage]
max_turns: 15
---

Triage my GitHub forks with the repo-review skill: `triage forks no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git` or WebFetch, and don't publish or save a page or keep a timing log. Everything those calls would return is given below; anything not given is unavailable.

The listing (`user/repos?affiliation=owner`), filtered to forks that aren't archived, has one repo:

```json
[{"full_name": "octo-dev/datepicker", "html_url": "https://github.com/octo-dev/datepicker", "private": false, "fork": true, "archived": false, "pushed_at": "2017-08-22T16:40:03Z", "stargazers_count": 0, "forks_count": 0, "open_issues_count": 0, "description": "A datepicker for Bootstrap", "topics": [], "size": 2210, "default_branch": "master", "license": {"spdx_id": "Apache-2.0"}}]
```

There is no previous triage page.

`gh api repos/octo-dev/datepicker --jq '.parent.full_name'` gives `picker-org/datepicker`. The repository search for the parent gives:

```json
{"total_count": 1, "items": [{"full_name": "picker-org/datepicker", "archived": false}]}
```

`gh api user --jq '.login, .name'` gives `octo-dev` and `Alex Rivera`.

Step 1's git commands for the fork print:

```
master
6
master	Alex Rivera	oldjob.example	2017-08-22	Build dist files
master	Alex Rivera	oldjob.example	2017-08-21	Style disabled dates for the booking form
master	Alex Rivera	oldjob.example	2017-08-21	Disable dates outside the booking window
master	Alex Rivera	oldjob.example	2017-08-18	Add a test for two-digit years
master	Alex Rivera	oldjob.example	2017-08-18	Keep the picker open while the month changes
master	Alex Rivera	oldjob.example	2017-08-17	Parse two-digit years in the en-GB locale
```

The search for my pull requests (`search/issues?q=author:octo-dev+type:pr+-user:octo-dev`) gives none to `picker-org/datepicker`.

Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Reply with triage's two lines. Then end with a JSON code block holding the triage page's `repos` array, each repo with `name`, `action`, `sure`, `reason` and, for `review`, `question`.
