---
description: An archived repo with every item before archiving done is recommended archive again, with nothing left to do.
tags: [review]
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/tidewatch with the repo-review skill, with `no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch or the quote checker, and don't publish or save a page or keep a timing log. Skip the outcomes, similar repos and the previous run. Everything the API and a clone would give is below; anything not given is unavailable.

`gh api repos/octo-dev/tidewatch`:

```json
{"full_name": "octo-dev/tidewatch", "private": false, "visibility": "public", "fork": false, "archived": true, "pushed_at": "2024-02-03T11:20:45Z", "description": "Tide predictions from harmonic constituents, in Python (archived, 2019 to 2023)", "topics": ["tides", "tide-prediction", "harmonic-analysis", "oceanography", "python"], "homepage": null, "has_issues": true, "license": {"spdx_id": "MIT"}, "default_branch": "main", "stargazers_count": 14, "forks_count": 2, "subscribers_count": 3, "open_issues_count": 0, "security_and_analysis": {"secret_scanning": {"status": "enabled"}, "secret_scanning_push_protection": {"status": "enabled"}}}
```

Open issues: 0. Open pull requests: 0. Open secret scanning alerts: none. Tags: `v1.2.0` (latest). Commits: all 212 by `octo-dev`. Checked at commit `9b7d03e`. Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Files: `README.md`, `LICENSE`, `pyproject.toml`, `tidewatch/__init__.py`, `tidewatch/constituents.py`, `tidewatch/predict.py`, `tidewatch/cli.py`, `tests/test_predict.py`, `tests/make_series.py`. The constituent speeds in `tidewatch/constituents.py` are computed from astronomical formulae in the code, and the tests use synthetic series that `tests/make_series.py` generates. No file is copied from another project, and there is no data or model file.

`LICENSE` line 1: `MIT License`; line 3: `Copyright (c) 2019 Octo Dev`.

`pyproject.toml` lines 1 to 7:

```toml
[project]
name = "tidewatch"
version = "1.2.0"
description = "Tide predictions from harmonic constituents"
requires-python = ">=3.7,<3.10"
dependencies = ["numpy==1.17.4", "scipy==1.3.3"]
license = "MIT"
```

`README.md`, with line numbers:

~~~markdown
1  > **No longer maintained.** This repo is archived; see [Status and history](#status-and-history).
2
3  # tidewatch
4
5  Predict the height of the tide at any port, from the harmonic constituents published for it. I wrote it to find out how close a few hundred lines of Python could get to the official tide tables: for Brest over 2022, its predicted high waters were within 6 cm and 4 minutes of the published ones.
6
7  ## Use
8
9  ```sh
10 pip install .
11 tidewatch predict --constituents brest.json --from 2022-01-01 --days 2
12 ```
13
14 Sample output:
15
16 ```text
17 2022-01-01 05:41  HW  6.12 m
18 2022-01-01 11:58  LW  1.43 m
19 2022-01-01 18:07  HW  5.88 m
20 ```
21
22 ## How it works
23
24 Each constituent is a cosine with a fixed speed, set by the motions of the Moon and Sun, and an amplitude and phase that differ from port to port. `tidewatch/predict.py` sums them, with the nodal corrections that move each constituent over the 18.6-year lunar node cycle.
25
26 ## Status and history
27
28 I wrote tidewatch between 2019 and 2023 as a way into harmonic analysis. It predicts well for ports with a strong semidiurnal tide and poorly for shallow-water ports, where higher harmonics matter; adding those was the next step, and I stopped before taking it when the sailing club I wrote it for switched to the official tables. If I started again I would fit the constituents from a port's own records rather than take published ones, which would have let me test the predictions against data I hadn't used.
29
30 UTide, which came before tidewatch, does the fitting as well as the prediction and is maintained: use it if you need a working tool (https://github.com/wesleybowman/UTide).
31
32 It doesn't run on current Python: it needs Python 3.9 or earlier, and I haven't updated it. Its pinned numpy and scipy have known vulnerabilities, so if you run it on an old Python, run it locally only.
33
34 ## Licence
35
36 MIT, see [LICENSE](LICENSE).
~~~

When you're done, end your reply with a JSON code block in this shape, with each question's status, the recommended action, and the items before that action (not those before featuring):

```json
{"statuses": {"Hook": "", "Findable": "", "Facts": "", "Evidence": "", "Jargon": "", "Getting started": "", "Tone": ""}, "action": "", "before": [{"text": "", "status": ""}]}
```
