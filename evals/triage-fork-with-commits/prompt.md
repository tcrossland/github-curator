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

`gh api repos/octo-dev/datepicker --jq .parent`:

```json
{"full_name": "picker-org/datepicker", "default_branch": "master", "archived": false}
```

`gh api 'repos/picker-org/datepicker/compare/master...octo-dev:master'`, with the commits as `.author.login`, the email domain and `.commit.message`:

```json
{"status": "diverged", "ahead_by": 6, "behind_by": 431, "commits": [
  {"login": null, "email_domain": "oldjob.example", "message": "Parse two-digit years in the en-GB locale"},
  {"login": null, "email_domain": "oldjob.example", "message": "Keep the picker open while the month changes"},
  {"login": null, "email_domain": "oldjob.example", "message": "Add a test for two-digit years"},
  {"login": null, "email_domain": "oldjob.example", "message": "Disable dates outside the booking window"},
  {"login": null, "email_domain": "oldjob.example", "message": "Style disabled dates for the booking form"},
  {"login": null, "email_domain": "oldjob.example", "message": "Build dist files"}
]}
```

`gh api --paginate 'repos/octo-dev/datepicker/commits?author=octo-dev&per_page=100' --jq '.[].sha' | wc -l` gives `0`.

`gh api 'search/issues?q=repo:picker-org/datepicker+author:octo-dev+type:pr'`:

```json
{"total_count": 0, "items": []}
```

Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Reply with triage's two lines. Then end with a JSON code block holding the triage page's `repos` array, each repo with `name`, `action`, `sure`, `reason` and, for `review`, `question`.
