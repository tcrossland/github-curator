---
description: Someone else's commits and a stranger's unanswered issue show in Outcomes, Tone is flagged when the README doesn't credit them, and the fix prompt drafts a reply.
tags: [review]
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/pgn-viewer with the repo-review skill, with `no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch, the quote checker or the scripts, and don't publish or save a page or keep a timing log. Skip similar repos, traffic, stargazers and the previous run. Everything the API, a clone and the scripts would give is below; anything not given is unavailable.

`gh api repos/octo-dev/pgn-viewer`:

```json
{"full_name": "octo-dev/pgn-viewer", "private": false, "visibility": "public", "fork": false, "archived": false, "pushed_at": "2026-06-02T19:44:10Z", "description": "View chess games from PGN files in the browser, with engine analysis of each move", "topics": ["chess", "pgn", "chess-engine", "stockfish", "web-app"], "homepage": "https://octo-dev.github.io/pgn-viewer", "has_issues": true, "license": {"spdx_id": "MIT"}, "default_branch": "main", "stargazers_count": 41, "forks_count": 6, "subscribers_count": 4, "open_issues_count": 1}
```

Tags: `v1.3.0` (latest). Checked at commit `5d81f0a`. Pinned on my profile: `octo-dev/tidewatch`, `octo-dev/ledgerlint`.

`people.py commits.tsv octo-dev` (Contributors):

```json
{"commits": 37, "user": 6, "others": [{"who": "kasia-dev", "login": true, "commits": 31, "last": "2026-06-02"}]}
```

`git log --format='%an %s' -- src/engine/` lists 14 commits, all by kasia-dev, from "Add Stockfish WASM worker" to "Show the engine's best line under the board".

Waiting on you (open issues and pull requests opened by someone else, with the user's replies):

```text
12	issue	chess-fan-99	2025-04-18	581 days	comments: 0	Board flips when loading a game with Black to move
```

Files: `README.md`, `LICENSE`, `package.json`, `src/` (`main.ts`, `board.ts`, `pgn.ts`, `engine/worker.ts`, `engine/analysis.ts`), `tests/`, `.github/workflows/ci.yml`. `LICENSE` line 3: `Copyright (c) 2023 Octo Dev`. `package.json` has `"license": "MIT"`, `"version": "1.3.0"` and a `test` script; CI runs `npm test` on every push.

`README.md`, with line numbers:

~~~markdown
1  # pgn-viewer
2
3  Paste a chess game in PGN and step through it on a board in your browser, with a chess engine's verdict on every move: where the game turned, and the move that was missed.
4
5  ![A game at move 23, with the engine's best line under the board](docs/screenshot.png)
6
7  Try it at https://octo-dev.github.io/pgn-viewer.
8
9  ## Why I built it
10
11 I built pgn-viewer because I wanted to see my own club games through an engine's eyes without uploading them anywhere. I wrote the PGN parser, the board and the engine analysis, which runs Stockfish in a web worker so nothing leaves your machine.
12
13 ## Run it locally
14
15 ```sh
16 npm install
17 npm run dev
18 ```
19
20 `npm test` runs the parser's tests against the games in `tests/games/`.
21
22 ## Licence
23
24 MIT, see [LICENSE](LICENSE).
~~~

When you're done, end your reply with a JSON code block in this shape: each question's status, the recommended action, the Contributors and Waiting on you entries as the scorecard would list them, and the fix prompt's items with their `question`, `status` and `text`:

```json
{"statuses": {"Hook": "", "Findable": "", "Facts": "", "Defensible": "", "Context": "", "Way in": "", "Tone": ""}, "action": "", "contributors": [""], "waiting": [""], "fixItems": [{"question": "", "status": "", "text": ""}]}
```
