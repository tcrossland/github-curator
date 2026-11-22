---
description: A private repo whose only Findable gap is its visibility is flagged on Findable, not failed.
tags: [review]
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/ledgerlint with the repo-review skill, with `no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch or the quote checker, and don't publish or save a page or keep a timing log. Skip the outcomes, similar repos and the previous run. Everything the API and a clone would give is below; anything not given is unavailable.

`gh api repos/octo-dev/ledgerlint`:

```json
{"full_name": "octo-dev/ledgerlint", "private": true, "visibility": "private", "fork": false, "archived": false, "pushed_at": "2026-10-30T18:02:11Z", "description": "Lint plain-text accounting journals for unbalanced entries, unknown accounts and out-of-order dates", "topics": ["plain-text-accounting", "ledger", "hledger", "beancount", "linter", "accounting"], "homepage": null, "has_issues": true, "license": {"spdx_id": "MIT"}, "default_branch": "main", "stargazers_count": 0, "forks_count": 0, "open_issues_count": 0}
```

Tags: `v0.3.0` (latest), `v0.2.0`, `v0.1.0`. Commits: all 58 by `octo-dev`. Checked at commit `4c1e9a2`. Pinned on my profile: `octo-dev/tidewatch`.

Files: `README.md`, `LICENSE`, `pyproject.toml`, `ledgerlint/__init__.py`, `ledgerlint/cli.py`, `ledgerlint/rules.py`, `tests/test_rules.py`, `tests/fixtures/sample.journal`, `.github/workflows/ci.yml`.

`LICENSE` line 1: `MIT License`; line 3: `Copyright (c) 2025 Octo Dev`.

`pyproject.toml` lines 1 to 6:

```toml
[project]
name = "ledgerlint"
version = "0.3.0"
description = "Lint plain-text accounting journals"
requires-python = ">=3.11"
license = "MIT"
```

`.github/workflows/ci.yml` runs `pytest` on Python 3.11, 3.12 and 3.13.

`README.md`, with line numbers:

~~~markdown
1  # ledgerlint
2
3  Catch the mistakes in a plain-text accounting journal before they reach your reports. ledgerlint reads ledger, hledger and beancount journals and reports unbalanced transactions, accounts that were never opened, and entries out of date order, each with its file and line.
4
5  On my own eight years of journals it found 41 problems, 3 of them unbalanced transactions that hledger had silently balanced with an inferred amount.
6
7  ## Install
8
9  ```sh
10 pip install git+https://github.com/octo-dev/ledgerlint
11 ```
12
13 ## Use
14
15 ```sh
16 ledgerlint path/to/main.journal
17 ```
18
19 Each problem is printed as `FILE:LINE: RULE: message`, and the exit status is 1 when any are found, so it can run in a pre-commit hook.
20
21 ## Rules
22
23 - `unbalanced`: a transaction's postings don't sum to zero in any commodity.
24 - `unopened`: a posting uses an account with no `open` (beancount) or `account` (ledger, hledger) directive.
25 - `order`: a transaction is dated before the one above it in the same file.
26
27 ## Tests
28
29 `pytest` runs the rules against `tests/fixtures/sample.journal`, which holds one example of each problem.
30
31 ## Licence
32
33 MIT, see [LICENSE](LICENSE).
~~~

The figures on line 5 come from my own journals, which aren't in the repo.

When you're done, end your reply with a JSON code block in this shape, with each question's status, the recommended action, and the items before that action (not those before featuring):

```json
{"statuses": {"Hook": "", "Findable": "", "Facts": "", "Evidence": "", "Jargon": "", "Getting started": "", "Tone": ""}, "action": "", "before": [{"text": "", "status": ""}]}
```
