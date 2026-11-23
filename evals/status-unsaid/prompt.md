---
description: "A README that says how to install, use and contribute, under a licence, but not whether the project is maintained, experimental or finished, has Getting started flagged, with a fix that states the status."
tags: [review]
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/tzshift with the repo-review skill, with `no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch, the quote checker or the scripts, and don't publish or save a page or keep a timing log. Skip the outcomes, similar repos, stargazers, forks and the previous run. Everything the API, a clone and the scripts would give is below; anything not given is unavailable.

`gh api repos/octo-dev/tzshift`:

```json
{"full_name": "octo-dev/tzshift", "private": false, "visibility": "public", "fork": false, "archived": false, "pushed_at": "2025-02-11T17:30:02Z", "description": "Convert timestamp columns in a CSV file from one time zone to another, daylight saving included", "topics": ["csv", "timezone", "cli", "datetime"], "homepage": null, "has_issues": true, "license": {"spdx_id": "MIT"}, "default_branch": "main", "stargazers_count": 5, "forks_count": 0, "subscribers_count": 1, "open_issues_count": 0}
```

Tags: `v0.3.0` (latest). Commits: all 29 by `octo-dev` (`people.py` lists no one else). Checked at commit `7b02d1e`. Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Files: `README.md`, `LICENSE`, `pyproject.toml`, `tzshift/__init__.py`, `tzshift/cli.py`, `tzshift/convert.py`, `tests/test_convert.py`, `.github/workflows/ci.yml`. `LICENSE` line 3: `Copyright (c) 2024 Octo Dev`. `pyproject.toml` has `version = "0.3.0"` and `requires-python = ">=3.10"`. CI runs `pytest` on Python 3.10 and 3.12 on every push; `tests/test_convert.py` includes `test_spring_forward_gap` and `test_fall_back_overlap`.

`README.md`, with line numbers:

~~~markdown
1  # tzshift
2
3  Shift the timestamp columns of a CSV file from one time zone to another, getting the daylight-saving changeovers right: a time that falls in the spring gap is moved forward, and one that occurs twice in the autumn takes the first occurrence unless you pass `--later`.
4
5  ## Install
6
7  ```sh
8  pip install git+https://github.com/octo-dev/tzshift
9  ```
10
11 ## Use
12
13 ```sh
14 tzshift orders.csv --column created_at --from Europe/London --to UTC > orders-utc.csv
15 ```
16
17 `--column` can be given more than once. Time zones are IANA names, such as `America/New_York`. The changeover rules are tested in `tests/test_convert.py`.
18
19 ## Contributing
20
21 Issues and pull requests are welcome. Run `pytest` before opening one.
22
23 ## Licence
24
25 MIT, see [LICENSE](LICENSE).
~~~

When you're done, end your reply with a JSON code block in this shape: each question's status, and the fix prompt's items with their `question`, `status` and `text`:

```json
{"statuses": {"Hook": "", "Findable": "", "Facts": "", "Evidence": "", "Jargon": "", "Getting started": "", "Tone": ""}, "fixItems": [{"question": "", "status": "", "text": ""}]}
```
