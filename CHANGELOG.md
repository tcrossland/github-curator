# Changelog

What changed for someone using the plugin, newest first. A Claude Code session keeps the version it started with, so start a new session after installing an update.

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
