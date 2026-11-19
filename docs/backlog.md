# Backlog

Ideas for the plugin, in the order to do them. Each says why it's worth doing and what done looks like. Anything not yet checked against its source is marked **unverified**.

## Summary

| # | Item | Kind | Size | Depends on | Status |
|---|---|---|---|---|---|
| 11 | [GitHub access from a claude.ai session](#11-github-access-from-a-claudeai-session) | Fix | M | none | todo |
| 1 | [Traffic history](#1-traffic-history) | New skill and scheduled task | M | 0 | todo |
| 2 | [Timing](#2-timing) | Measurement | S | 0 | in progress |
| 3 | [Split `SKILL.md` by mode](#3-split-skillmd-by-mode) | Restructure | S | 0 | todo |
| 4 | [Quick review](#4-quick-review) | New mode | M | 2, 3 | todo |
| 5 | [Benchmark against good practice](#5-benchmark-against-good-practice) | Scorecard panel | L | 3 | todo |
| 6 | [Profile review](#6-profile-review) | New skill | M | 0 | todo |
| 7 | [Behaviour evals](#7-behaviour-evals) | Tests | M | 3 | todo |
| 8 | [Forks](#8-forks) | New skill | M | none | todo |
| 9 | [Secrets scanner for publishing](#9-secrets-scanner-for-publishing) | Checklist tool | M | licence check | todo |
| 10 | [Launch drafts](#10-launch-drafts) | New skill | M | 1 helps | todo |
| – | [Smaller items](#smaller) | Fixes | S each | none | todo |
| 0 | [Prove the current version on claude.ai](#done) | Check | S | none | done |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` or `done` as work moves, and move a done item's section to the end, or delete it once the summary row says enough.

## 11. GitHub access from a claude.ai session

The 0.2.4 test runs on claude.ai (see Done, below) showed that the session's `gh` is bound to the repos attached to it. GraphQL, `user/repos`, every `users/…` and `orgs/…` path, and `repos/OWNER/REPO` for any repo not attached are all refused with HTTP 403. The facts are in `docs/github-facts.md`. What each mode lost:
- **Triage** listed its repos through `list_repos` and took their fields from the search API, but couldn't read a README or compare a fork with its parent, so it marked no repo clear. On claude.ai it's a list, not a triage.
- **Stargazers** listed the stargazers but couldn't read a single profile, so it couldn't pick the ones worth a look, in the skill or in the review's Outcomes panel.
- **Similar repos** described each repo from its search result, because other owners' READMEs were refused.

Three more probes tested the routes around this (facts in `docs/github-facts.md`). What they settled:
- **Attaching works only with push access, and only with the user's permission.** Read access gives an anonymous git clone and nothing more. With the user's permission one session attached 12 repos with push access, and an attached fork's `.parent` can be read. In auto mode, push access is refused unless the user asked for it.
- **Cross-fork compare is out**, even for an attached fork: the proxy refuses it with HTTP 400.
- **Git works** for any public repo without attaching it, through the session's proxy as in Claude Code: a sparse clone of just the README, and a fork's count beyond its parent from treeless clones.
- **WebFetch isn't a source of exact text**: it reworded and cut a README, and was rate-limited on repo pages. A profile through it gives the name, followers and pinned repos only.
- **Issue search answers**, so the user's merged pull requests to a parent can still be read.

The route, the same in both places where it can be:
- **READMEs** (triage's own repos, similar repos): a sparse clone that checks out only the README.
- **A fork against its parent**: the count and the authors from treeless clones, `git rev-list --count` and `git log`. This also lifts the compare API's limit of 250 commits. A parent as large as elixir's still costs its whole commit history.
- **A fork's parent**: only `gh api repos/OWNER/FORK` gives it, which on claude.ai needs the fork attached with push access; `list_repos`, search and GraphQL don't (a third probe checked all three). A parent doesn't change, so the triage page records each fork's parent and its default branch, and a later triage reads them from the previous page, as it already reads that page to compare. Only forks new since then need the API. The first triage on claude.ai either attaches every fork, with the user's permission, or is run from Claude Code instead, where the user's own `gh` reads every parent; the page says which.
- **Pull requests to the parent**: issue search, as now.
- **Stargazers' profiles**: WebFetch of `github.com/LOGIN`, one at a time, judging the field from the pinned repos' descriptions, labelled "profile page summary". Say in the reply that bio, company and location weren't available.
- **Private repos** need attaching too.
- **On claude.ai, triage asks once for permission to attach** the forks whose parent it doesn't know yet and the private repos, and leaves any it can't attach as `review`, saying which and why.

Still **unverified**: whether a session can attach more than 12 repos. It matters only for a first triage on claude.ai with no previous page to read parents from (62 forks and 10 private repos on this account).

**Done when** triage on claude.ai marks the clear deletes it marks in Claude Code on the same account, and stargazers there reads profiles or says plainly that it can't.

## 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

A scheduled task would save the stars, views, clones and top referrers of every public repo, once a week, to an artifact with a shared database, and chart the trend. The scorecard's outcomes panel could then link to it.

**Unverified**: that scheduled tasks and artifact databases are available where the plugin runs, and that the scheduled task gets the push access traffic needs.

**Done when** two weekly snapshots of every public repo are saved and charted on the page.

## 2. Timing

Nothing records how long a run takes or where the time goes. A full review clones the repo, makes many `gh api` calls, searches for similar repos and reads one profile per stargazer; triage makes several calls per fork. Measure before speeding anything up or adding a faster mode (item 4).

Have each mode record, at the start and end of every step, the time from the shell (`date -u +%s`) and the number of `gh api` calls made, and put them in the page's JSON as `timings`: a list of `{step, seconds, calls}`. The template shows them in a closed section at the foot of the page; overview and triage also give the totals. The times include Claude's own work between tool calls, which is what the user waits for, but can't separate it from time spent waiting on GitHub. A skill can't read its own token use.

The shell's clock on claude.ai is wall-clock (`docs/github-facts.md`).

**First figures**, timed by hand in the 0.2.4 test runs, before the skill logged anything (runs 1 and 2 rebuilt from file and publish times, to about ±10 seconds): about 682 s across the four runs. In every run the time went to Claude's own work between calls, not to waiting on GitHub:
- review of spacy-annotator: about 310 s, slowest building the run and checking its quotes and numbers (Steps 3 and 4, about 95 s);
- overview of two repos: about 236 s, slowest Step 1 and Steps 2 to 4, about 70 s each;
- triage: 105 s, slowest the signals (37 s), though most of its reads were refused (item 11);
- stargazers: 31 s, slowest reading profiles (12 s), all refused.

**Status**: the skill and template side is in. `SKILL.md` has a Timing section: each step appends its name, `date -u +%s` and the rate limit's `core.used` to a log, and a script turns the log into `timings`, with `calls` read from the rate limit (which costs no request) rather than counted by hand. Search requests aren't in `core.used`, so they're counted by hand as `searches`. The template shows the rows and a total in a closed section above the footer, in all three modes. What's left is a release with it and the runs below. `gh api rate_limit` answers on claude.ai and counts calls there; its count is shared with anything else using the account at the same time (`docs/github-facts.md`).

**Done when** a review, an overview and a triage each show per-step times on their pages, and the slowest step of each is written up here, as a candidate to speed up.

## 3. Split `SKILL.md` by mode

`skills/repo-review/SKILL.md` is about 300 lines (40 KB), and every run loads all of it, including the overview and triage steps that a single review never uses. Move Step 7 (overview) and Step 8 (triage) into supporting files beside it, linked from the modes list and read only in those modes. Item 5 would add more to the file, so do this first.

**Done when** a single review loads only the shared rules and Steps 1 to 6, the overview and triage files are linked by relative path, and the tests still pass.

## 4. Quick review

A `quick` mode that reads only the API and the README, with no clone, quote checker, stargazers or search for similar repos, and answers the questions those can settle: Hook (the description and the README's opening), Findable (description and topics) and Way in (a licence, and whether the README says how to run it). It gives each repo a row of statuses and signals, not a page of its own, and its results are provisional, as triage's are.

Uses:
- **Similar repos** in a full review: a quick review of each says what it does better than the repo under review (a clearer opening, the topics people search for), where today the panel has only their descriptions.
- **Triage's repos to review**: rank them by a quick pass before spending full reviews on them.
- **Overview of many repos**, when a full review of each would take too long.

**Done when** a quick review of ten repos takes a small part of the time an overview of the same ten takes (from item 2's timings), and its Hook, Findable and Way in statuses agree with the full reviews' on those repos, with each disagreement explained.

## 5. Benchmark against good practice

The review checks the page, not the engineering. A visitor who opens `pyproject.toml` or the CI workflow judges the craft too, and nothing checks it today: the manifest, CI workflow and licence are read only to confirm facts on the page.

Add a **Practice** panel to the scorecard: a checklist of `done`, `todo` and `n/a`, each with its evidence, kept apart from the seven questions so it doesn't blur them. Its `todo` items join the fix prompt. It also feeds into Way in, Tone and the feature call.

- **Common to every repo**: a README with what it is, how to install and run it, and the result; a licence (already checked under Way in, so the panel only refers to that finding); tests, and CI that runs them on every push; a CI badge only when the badge is accurate; tagged releases and a changelog when it's versioned; CONTRIBUTING and issue templates only when it invites contributions. GitHub's community profile (`gh api repos/OWNER/REPO/community/profile`) reports most of the files and a health percentage.
- **One profile per ecosystem**, detected from the manifest and kept in its own file (`skills/repo-review/practice/python.md` and so on), so a profile can be updated without touching the skill. For Python:
  - `pyproject.toml` with standard project metadata, including `requires-python`;
  - one tool chain used throughout, with a lockfile committed; uv is the default suggestion for an active repo;
  - lint and format configuration (for example ruff);
  - type checking when the code is typed;
  - a test runner that CI runs;
  - dependency licences read from each dependency's own metadata, flagging any copyleft or non-commercial terms that conflict with the repo's licence.

  JavaScript and TypeScript, then Elixir, would follow.
- **Judged against the repo's era and action**: an archived 2017 repo isn't marked down for 2017 tooling. For archive, only "says how to run it, or that it no longer runs" applies, as in the checklist before archiving.
- **Standards over fashion**: mark missing standard pieces (no `pyproject.toml`, no lockfile, tests CI doesn't run) as `todo`. Suggest uv, but don't mark down a repo that uses another current tool consistently.
- Each profile carries the date it was last reviewed, since good practice moves quickly.

**Done when** a review of a Python repo with a `pyproject.toml` and CI shows a Practice panel whose items match those files, with evidence for each, and `tests/` holds small fixture repos with known Practice results, one per profile, so a change to a profile can't silently break it.

## 6. Profile review

The profile page is the first thing a visitor sees. A profile README (the `OWNER/OWNER` repo), the bio, the pins and the featured repos aren't checked together today.

A new skill, `profile-review`, would:
- check the bio and the pins, reusing the pin ranking from overview mode;
- draft a short profile README in the house style that introduces the featured repos;
- publish a scorecard like the repo review's.

**Done when**, for a real profile, it produces:
- a pins recommendation that names what to pin and what to drop, with a reason for each;
- a draft profile README that links every recommended pin, and would read well to a visitor who has never heard of the user.

## 7. Behaviour evals

The tests cover code (the quote checker and the template), not the skill's judgement. A change to a rule could flip a recommendation without anything noticing. Keep a few known cases, each with the input and the expected call:
- an unchanged fork nobody uses is a clear delete in triage;
- a fork with commits beyond its parent is never clear;
- a private repo never fails Findable on visibility alone;
- an archived repo with every item done is recommended archive, with nothing to do.
- the same commit gets the same statuses twice. In the 0.2.4 test runs, claude-code-methodology's Way in was flagged in one review and passed in the next, on the same commit, so a case that runs one repo twice would catch a rule that leaves too much to judgement.

Claude Code has a `claude plugin eval` command that reads cases from `evals/` by default. **Unverified**: how its cases and checks are written.

**Done when** the cases above run with one command, and each fails if its rule is removed from `SKILL.md`.

## 8. Forks

A fork with commits says more than a star: someone used the code. This would be the `stargazers` skill's counterpart. It would list the forks that have commits beyond the user's repo, what they changed and who changed it. Its rules would match: public data only, never contact anyone. It would also tell triage how much others rely on a repo.

**Done when** it runs on a repo with forks, lists each fork's commits beyond the original with their authors, and is called from the repo review's outcomes panel.

## 9. Secrets scanner for publishing

The secrets check before publishing relies on the model reading `git log`, which is weak over a long history. Use a dedicated scanner instead. Candidates, neither licence yet read from the project itself (**unverified**):
- gitleaks, believed MIT;
- trufflehog, believed AGPL-3.0.

AGPL is copyleft, so read the licences before adding either. Calling a tool installed on the machine is different from bundling it.

**Done when** the before-publishing check runs a scanner over the full history and reports each finding with its commit and file, and a test repo with a planted fake key is caught.

## 10. Launch drafts

When the review says publish or feature, draft the announcement: where it fits, and a post for each place, in the house style. It drafts only: posting is the user's call. Traffic history (item 1) would show which places brought visitors before.

**Done when**, for one repo recommended for featuring, it drafts posts for at least two places, each with the reason it fits (from the repo's referrers or where similar repos are discussed).

## Smaller

Each is done when the change is made and the tests pass, unless it says otherwise.

- **Three most-starred repos in `stargazers`**: it reads the first 100 repos only, and the API can't sort them by stars, so for someone with more than 100 repos the three can be wrong. Paginate, then sort by stars.
- **Quote checker as a file**: move the quote checker from `SKILL.md` into `skills/repo-review/verify_run.py`, so it's run rather than retyped, and point `tests/test_verify_run.py` at the new file.
- **Author identities**: let the user list their past commit email domains, kept outside the plugin (in a gitignored file or an environment variable), so triage can tell their unlinked commits from other people's without asking. Done when triage reads the list and marks matching commits as the user's.
- **Recheck the traffic claim**: `docs/github-facts.md` marks "14 days, needs push access" as not rechecked. Done when it has a source and a date.
- **Rate limits in triage**: the pull-request search goes through GitHub's search API, whose rate limit is far lower than the rest of the API's, so an account with many forks that have commits could hit it. Say in Step 8 to pace the searches and to note any that were refused. Done when triage on an account with more than 30 such forks completes.
- **Stargazers when profiles can't be read**: neither skill says what to do when Step 2 of `stargazers` can't read the profiles, so the scorecard falls back to "None in the same field", which reads as a judgement that was never made (seen in the 0.2.4 test runs, where every profile call was refused). Say "Not available" with the reason instead, in the `stargazers` reply and in the review's Stargazers lists. Done when both skills say so, and a template test checks the scorecard's wording.
- **Fix prompts on the overview**: the overview page links each repo's scorecard but has no fix prompt, so acting on an overview means opening each scorecard in turn. Add a copy button to each row that has failing or flagged questions, copying that repo's fix prompt as its scorecard builds it (`fixPrompt` with every item). Keep one prompt per repo, not one for all of them: each runs in its own Claude Code session in that repo. Done when the overview's JSON carries each repo's `fixPrompt`, each row's button copies the same text as its scorecard's "All", and a template test checks it.
- **README links that don't ship**: the README is in the zip, but its "Working on it" section links to `docs/`, which isn't. Move that section to `docs/README.md`, or have `scripts/package.sh` leave it out.

## Done

### 0. Prove the current version on claude.ai

0.2.4 was uploaded and every mode run once on 2026-11-19, recorded in the doc "github-curator 0.2.4: test report". Each run finished and published:
- the review of spacy-annotator recommended archive and keeping it pinned, with all seven questions passing, and one item before archiving still to do, where none was expected: third-party text in the repo with no source named. That's a finding about the repo, not a fault in the plugin;
- the overview of stat-arb-from-scratch and claude-code-methodology passed;
- triage listed 82 repos through the `list_repos` fallback, but marked none clear (item 11);
- stargazers listed 13 stargazers but read no profiles (item 11, and the smaller item on what to show then).

The scorecard template loaded through its relative link, pins came through WebFetch, GraphQL is refused, and `argument-hint` caused no trouble. Each is now in `docs/github-facts.md`.
