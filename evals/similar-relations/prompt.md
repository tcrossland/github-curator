---
description: Similar repos say what the user's repo adds without judging the others, and Mention follows from how the repos relate.
tags: [review]
max_turns: 15
---

Review my GitHub repo https://github.com/octo-dev/pairtrade-lab with the repo-review skill, with `no-publish`. My GitHub login is `octo-dev`.

This is an offline test of the skill's rules. There is no shell, network or artifact tool here, so don't run `gh`, `git`, WebFetch or the quote checker, and don't publish or save a page or keep a timing log. Run only Step 1's reading of the repo and Similar repos, from what's below; skip the outcomes, the seven questions, the recommendation and the previous run. Everything the API, the searches and the README clones would give is below; anything not given is unavailable. Today is 2026-11-22.

`gh api repos/octo-dev/pairtrade-lab`:

```json
{"full_name": "octo-dev/pairtrade-lab", "private": false, "fork": false, "archived": false, "created_at": "2025-02-14T09:12:40Z", "pushed_at": "2026-09-30T18:03:11Z", "description": "Pairs trading on US equities, with costs, counting every parameter tried against a deflated Sharpe ratio", "topics": ["pairs-trading", "backtesting", "deflated-sharpe-ratio"], "license": {"spdx_id": "MIT"}, "stargazers_count": 4}
```

`README.md` lines 1 to 9 (the README names no other project anywhere):

~~~markdown
1  # pairtrade-lab
2
3  Does pairs trading on US equities still pay once costs are paid and every parameter I tried is counted? Not reliably: the best pair set made a Sharpe ratio of 0.31 after costs, and its deflated Sharpe ratio, which allows for the 240 configurations I tried, is 0.12.
4
5  ## What it does
6
7  - Picks pairs by cointegration on a formation window, then trades them on the next window, with no look-ahead.
8  - Charges commission, spread and borrow on every trade.
9  - Logs every configuration tried, so the deflated Sharpe ratio counts them all.
~~~

The topic search, `search/repositories?q=topic:pairs-trading+topic:backtesting&sort=stars&per_page=10`, and the word search, `search/repositories?q=pairs+trading+in:name,description,topics&sort=stars&per_page=10`, together found these two that do the same job (the rest were lists and course notes):

```json
[
  {"full_name": "quantfolk/pairs-trading", "html_url": "https://github.com/quantfolk/pairs-trading", "stargazers_count": 940, "created_at": "2019-04-02T11:00:00Z", "pushed_at": "2026-10-20T08:30:00Z", "archived": false, "description": "Pairs trading strategies on US equities in Python", "topics": ["pairs-trading", "quantitative-finance", "python", "backtesting"]},
  {"full_name": "oldquant/pairs-backtest", "html_url": "https://github.com/oldquant/pairs-backtest", "stargazers_count": 310, "created_at": "2016-01-10T15:45:00Z", "pushed_at": "2017-06-01T10:00:00Z", "archived": true, "description": "Backtest of pairs trading on S&P 500 stocks", "topics": ["pairs-trading", "backtest", "sp500"]}
]
```

Their README openings, from the clones:

~~~markdown
== README.md   (quantfolk/pairs-trading)
# pairs-trading

Pairs trading in Python, after Gatev, Goetzmann and Rouwenhorst (2006).
~~~

~~~markdown
== README.md   (oldquant/pairs-backtest)
# pairs-backtest

Archived. The results below were never checked against trading costs and shouldn't be relied on.

| Sharpe ratio | 2.4 |
~~~

When you're done, end your reply with a JSON code block in this shape, one object per similar repo, keys in this order:

```json
{"similar": [{"name": "", "overlap": "", "alive": "", "mention": "", "difference": ""}]}
```
