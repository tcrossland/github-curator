# Changelog

What changed for someone using the plugin, newest first. A Claude Code session keeps the version it started with, so start a new session after installing an update.

## 0.2.14 (2026-11-20)

- `repo-review` says what to use in Claude Code in place of each claude.ai tool, and saves the page as a file when there's no artifact tool to publish it with.
- Step 1 says where GraphQL works for reading the profile's pins, rather than calling it unavailable and then using it.
- The review's JSON starts in Step 4, with the questions the quote checker reads, and its timings count that writing in Step 4's row.

## 0.2.13 (2026-11-20)

- A single review loads less: the overview and triage steps are in files of their own, read only in those modes, so the review's instructions are about a fifth shorter.
- The quote checker ships as a file, `verify_run.py`, and is run as written rather than retyped from the instructions.

## 0.2.12 (2026-11-20)

- `stargazers` finds a stargazer's three most-starred repos, and their organisation's, among all of them. Before, it looked only at the first 100, so for someone with more it could miss their best-known work.

## 0.2.11 (2026-11-20)

- The README that comes with the plugin no longer links to notes that aren't in it.

## 0.2.10 (2026-11-20)

- Timings split a run's time between its steps more truly: each step's time is logged on its own as soon as the step ends. Before, the work of the next step could be counted to the one before it.

## 0.2.9 (2026-11-20)

- Timings give an API call count on more rows. GitHub's rate limit can give slightly different reset times, or now and then a stray count, within one hour, and each blanked the count on rows where GitHub's hourly window hadn't reset. Now only a stray count's two rows go without.

## 0.2.8 (2026-11-20)

- A review's Timings know that GitHub doesn't count traffic requests, so the Outcomes row's API calls leave out its four requests for views, clones, referrers and pages, and a run says so rather than guessing.

## 0.2.7 (2026-11-20)

- An overview reviews its repos one at a time, so each scorecard's Timings and the overview's time per repo are that repo's own. Before, reviews could run side by side, and their times and API calls ran together.

## 0.2.6 (2026-11-20)

- The reply to a review or an overview takes its pass, fail and flagged counts from the page's own data, so the reply and the page always agree. Before, they were counted by hand and could differ.

## 0.2.5 (2026-11-19)

- Every scorecard, overview and triage page has a Timings section at its foot: how long each step took and how many GitHub API calls it made, with totals. It's closed until opened.

## 0.2.4 (2026-11-19)

- `repo-review triage org:NAME` triages an organisation's repos, more strictly than your own, on a page of its own.
- `no-publish` in any `repo-review` mode saves each page as a file instead of publishing it.
- `stargazers` with no repo covers every public repo of yours that has stars. `since:YYYY-MM-DD` keeps only recent stars, and `all` reads every stargazer, not only the 30 most recent.
- Both skills show their arguments in Claude Code's autocomplete.

## 0.2.3 (2026-11-19)

- `stargazers` no longer mistakes someone else's public repo for a private one. GitHub lists stargazers only to a repo's owner, so for another owner's repo it now says the list is hidden and gives the public star count. The review's Outcomes panel shows the same gap.

## 0.2.2 (2026-11-19)

- The fix prompt follows the repo's own rules and your instructions on branches. Without either, a public repo, or one others commit to, still gets a branch and a pull request, and a private repo only you commit to gets unpushed commits on the current branch.

## 0.2.1 (2026-11-19)

- Way in fails a repo with no licence file, one whose README or manifest names a licence no file holds, and one whose licence still has a template's placeholder copyright line.
- Featuring now needs a licence. Archiving and publishing need a known source, with terms that allow redistribution, for any third-party data or model files.
- Triage marks your own repos that have no licence.

## 0.2.0 (2026-11-19)

- First release: `repo-review`, with its `overview` and `triage` modes, and `stargazers`.
