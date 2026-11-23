---
description: "With `for:users`, the same repo passes Jargon, since a practitioner knows the field's terms, and Tone isn't met, since nothing says its status, what it supports or where to get help."
tags: [review, audience]
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/transit-hunt with the repo-review skill, with `no-publish` and `for:users`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch, the quote checker or the scripts, and don't publish or save a page or keep a timing log. Skip the outcomes, similar repos, stargazers, forks and the previous run. Everything the API, a clone and the scripts would give is below; anything not given is unavailable.

`gh api repos/octo-dev/transit-hunt`:

```json
{"full_name": "octo-dev/transit-hunt", "private": false, "visibility": "public", "fork": false, "archived": false, "pushed_at": "2026-03-09T21:12:44Z", "description": "Find exoplanet transits in TESS light curves and fit each candidate", "topics": ["exoplanets", "tess", "transit-search", "astronomy", "python"], "homepage": null, "has_issues": true, "license": {"spdx_id": "MIT"}, "default_branch": "main", "stargazers_count": 9, "forks_count": 1, "subscribers_count": 2, "open_issues_count": 0}
```

Tags: `v1.0.0` (latest). Commits: all 64 by `octo-dev` (`people.py` lists no one else). Checked at commit `a41c9e2`. Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

Files: `README.md`, `LICENSE`, `pyproject.toml`, `transit_hunt/` (`__init__.py`, `cli.py`, `detrend.py`, `search.py`, `fit.py`), `bench/known.csv` (40 rows: TIC ID, planet name, published period), `bench/recover.py`, `tests/`, `docs/toi700d.png`, `.github/workflows/ci.yml`. `LICENSE` line 3: `Copyright (c) 2026 Octo Dev`. `pyproject.toml` has `version = "1.0.0"` and `requires-python = ">=3.11"`. CI runs `pytest` on Python 3.12 on every push. `bench/recover.py` runs the search on each row of `bench/known.csv` and prints, for each planet, the period found and whether it is within 0.1% of the published one; its last run, saved in `bench/results.txt`, ends `recovered 38 of 40`.

`README.md`, with line numbers:

~~~markdown
1  # transit-hunt
2
3  Finds exoplanet transits in TESS light curves: give it a TIC ID and it returns each planet candidate it finds, with its period, depth and duration, and a plot of the fit.
4
5  ![Phase-folded light curve of TOI-700 d with the fitted transit model](docs/toi700d.png)
6
7  On the 40 confirmed planets in `bench/known.csv` it recovers 38 at the published period, to within 0.1% (`python bench/recover.py`, results in `bench/results.txt`).
8
9  ## How it works
10
11 It detrends each light curve with a biweight filter, runs a BLS periodogram, keeps peaks above SNR 7, and fits each candidate with a Mandel-Agol model with quadratic limb darkening.
12
13 ## Why I built it, and what I learned
14
15 I built transit-hunt over a winter to learn how a planet search works from raw light curve to fitted candidate. The hardest part was detrending: a window shorter than about three transit durations ate the transits themselves, and the two planets it still misses are long-period ones where that trade-off bites. I learned to test each stage on planets whose answer is known before trusting it on anything new, which is what `bench/` is for.
16
17 ## Run it
18
19 ```sh
20 pip install .
21 transit-hunt TIC 150428135
22 ```
23
24 ```text
25 candidate 1  period 37.42 d  depth 810 ppm  duration 3.2 h  SNR 11.4
26 ```
27
28 ## Licence
29
30 MIT, see [LICENSE](LICENSE).
~~~

When you're done, end your reply with a JSON code block in this shape: each question's status, and the fix prompt's items with their `question`, `status` and `text`:

```json
{"statuses": {"Hook": "", "Findable": "", "Facts": "", "Evidence": "", "Jargon": "", "Getting started": "", "Tone": ""}, "fixItems": [{"question": "", "status": "", "text": ""}]}
```
