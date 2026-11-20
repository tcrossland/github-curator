---
description: An unchanged fork that nobody else uses is a clear delete in triage.
tags: [triage]
max_turns: 15
---

Triage my GitHub forks with the repo-review skill: `triage forks no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git` or WebFetch, and don't publish or save a page or keep a timing log. Everything those calls would return is given below; anything not given is unavailable.

The listing (`user/repos?affiliation=owner`), filtered to forks that aren't archived, has one repo:

```json
[{"full_name": "octo-dev/vue-range-slider", "html_url": "https://github.com/octo-dev/vue-range-slider", "private": false, "fork": true, "archived": false, "pushed_at": "2019-04-11T09:12:44Z", "stargazers_count": 0, "forks_count": 0, "open_issues_count": 0, "description": "A range slider component for Vue", "topics": [], "size": 412, "default_branch": "master", "license": {"spdx_id": "MIT"}}]
```

`gh api repos/octo-dev/vue-range-slider --jq .parent`:

```json
{"full_name": "slider-works/vue-range-slider", "default_branch": "master", "archived": false}
```

`gh api 'repos/slider-works/vue-range-slider/compare/master...octo-dev:master'`:

```json
{"status": "behind", "ahead_by": 0, "behind_by": 212, "commits": []}
```

`gh api 'search/issues?q=repo:slider-works/vue-range-slider+author:octo-dev+type:pr'`:

```json
{"total_count": 0, "items": []}
```

Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Reply with triage's two lines. Then end with a JSON code block holding the triage page's `repos` array, each repo with `name`, `action`, `sure`, `reason` and, for `review`, `question`.
