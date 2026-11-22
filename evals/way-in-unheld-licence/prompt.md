---
description: A README that names a licence no file holds fails Getting started, the same way on every run.
tags: [review, repeat]
runs: 3
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/csvdiff-lite with the repo-review skill, with `no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch or the quote checker, and don't publish or save a page or keep a timing log. Skip the outcomes, similar repos and the previous run. Everything the API and a clone would give is below; anything not given is unavailable.

`gh api repos/octo-dev/csvdiff-lite`:

```json
{"full_name": "octo-dev/csvdiff-lite", "private": false, "visibility": "public", "fork": false, "archived": false, "pushed_at": "2026-09-14T08:51:30Z", "description": "Diff two CSV files by key column, showing added, removed and changed rows", "topics": ["csv", "diff", "cli", "data-quality"], "homepage": null, "has_issues": true, "license": null, "default_branch": "main", "stargazers_count": 3, "forks_count": 0, "open_issues_count": 0}
```

Tags: `v0.4.1` (latest). Commits: all 37 by `octo-dev` (`contributors?anon=1` lists only `octo-dev`). Checked at commit `e21f0c7`. Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Files: `README.md`, `pyproject.toml`, `csvdiff_lite/__init__.py`, `csvdiff_lite/cli.py`, `csvdiff_lite/diff.py`, `tests/test_diff.py`, `.github/workflows/ci.yml`. There is no `LICENSE`, `COPYING` or other licence file.

`pyproject.toml` lines 1 to 5:

```toml
[project]
name = "csvdiff-lite"
version = "0.4.1"
description = "Diff two CSV files by key column"
requires-python = ">=3.10"
```

`.github/workflows/ci.yml` runs `pytest` on Python 3.12.

`README.md`, with line numbers:

~~~markdown
1  # csvdiff-lite
2
3  Compare two exports of the same table and see exactly which rows were added, removed or changed, matched on a key column instead of line by line. A reordered export shows no differences, and a changed row shows only the cells that changed.
4
5  ## Install
6
7  ```sh
8  pip install git+https://github.com/octo-dev/csvdiff-lite
9  ```
10
11 ## Use
12
13 ```sh
14 csvdiff-lite old.csv new.csv --key id
15 ```
16
17 ```text
18 + 1042  added
19 - 0977  removed
20 ~ 1001  email: a@example.com -> b@example.com
21 ```
22
23 `--key` takes several columns separated by commas for a compound key. The exit status is 1 when the files differ.
24
25 ## Contributing
26
27 Issues and pull requests are welcome. Run `pytest` before opening one.
28
29 ## Licence
30
31 MIT.
~~~

When you're done, end your reply with a JSON code block in this shape, with each question's status, the recommended action, and the items before that action (not those before featuring):

```json
{"statuses": {"Hook": "", "Findable": "", "Facts": "", "Evidence": "", "Jargon": "", "Getting started": "", "Tone": ""}, "action": "", "before": [{"text": "", "status": ""}]}
```
