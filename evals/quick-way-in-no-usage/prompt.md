---
description: A quick review fails Getting started for a README with a licence and no word on how to install, run or use the repo.
tags: [quick]
max_turns: 15
---

Run a quick review of my repo https://github.com/octo-dev/tilegen with the repo-review skill: `quick https://github.com/octo-dev/tilegen no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, `jq` or the quote checks, and don't publish or save a page or keep a timing log. Skip the pinned repos and the previous quick review. Everything the search and the README clone would give is below; anything not given is unavailable.

`gh api 'search/repositories?q=repo:octo-dev/tilegen+fork:true&per_page=100' | jq -c '.items[]'`:

```json
{"full_name": "octo-dev/tilegen", "html_url": "https://github.com/octo-dev/tilegen", "private": false, "fork": false, "archived": false, "size": 412, "pushed_at": "2026-10-02T17:20:11Z", "stargazers_count": 9, "forks_count": 1, "open_issues_count": 0, "description": "Cut map tiles from a GeoTIFF at every zoom level, so a static site can serve a slippy map with no tile server", "topics": ["map-tiles", "geotiff", "slippy-map", "static-site"], "license": {"key": "mit", "spdx_id": "MIT", "name": "MIT License"}, "has_issues": true}
```

Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

The README clone printed `== README.md`. `README.md`, with line numbers, is the whole file:

~~~markdown
1  # tilegen
2
3  Cut map tiles from a GeoTIFF at every zoom level, so a static site can serve a slippy map straight from object storage, with no tile server to run or pay for.
4
5  ## Why
6
7  Tile servers are the expensive part of a small map. Most maps I make change once a year, so the tiles can be cut once and served as plain files.
8
9  ## How it works
10
11 It reprojects the GeoTIFF to Web Mercator, then writes one PNG per tile in the `z/x/y.png` layout every slippy-map library reads. Empty tiles are skipped, which keeps a regional map to a few thousand files.
12
13 ## Licence
14
15 MIT. See `LICENSE`.
~~~

When you're done, end your reply with a JSON code block in this shape, with the quick review's three statuses for the repo and its likely action:

```json
{"statuses": {"Hook": "", "Findable": "", "Getting started": ""}, "action": ""}
```
