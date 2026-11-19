# Backlog

Ideas for the plugin, in the order to do them. Each says why it's worth doing and what done looks like. Anything not yet checked against its source is marked **unverified**.

## Summary

| # | Item | Kind | Size | Depends on | Status |
|---|---|---|---|---|---|
| 0 | [Prove the current version on claude.ai](#0-prove-the-current-version-on-claudeai) | Check | S | none | todo |
| 1 | [Traffic history](#1-traffic-history) | New skill and scheduled task | M | 0 | todo |
| 2 | [Timing](#2-timing) | Measurement | S | 0 | todo |
| 3 | [Split `SKILL.md` by mode](#3-split-skillmd-by-mode) | Restructure | S | 0 | todo |
| 4 | [Quick review](#4-quick-review) | New mode | M | 2, 3 | todo |
| 5 | [Benchmark against good practice](#5-benchmark-against-good-practice) | Scorecard panel | L | 3 | todo |
| 6 | [Profile review](#6-profile-review) | New skill | M | 0 | todo |
| 7 | [Behaviour evals](#7-behaviour-evals) | Tests | M | 3 | todo |
| 8 | [Forks](#8-forks) | New skill | M | none | todo |
| 9 | [Secrets scanner for publishing](#9-secrets-scanner-for-publishing) | Checklist tool | M | licence check | todo |
| 10 | [Launch drafts](#10-launch-drafts) | New skill | M | 1 helps | todo |
| – | [Smaller items](#smaller) | Fixes | S each | none | todo |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` or `done` as work moves, and move a done item's section to the end, or delete it once the summary row says enough.

## 0. Prove the current version on claude.ai

Build the zip with `scripts/package.sh`, upload it, and run every mode once before building more:
- `repo-review` on a repo whose expected result is already known, such as one already brought up to the checklist and archived;
- `repo-review overview` on two or three repos;
- `repo-review triage`, which also checks that `gh api user/repos` lists private repos in that environment, or that the `list_repos` fallback works;
- `stargazers` on a repo with stars.

Also check along the way:
- The scorecard template loads through the relative link in Step 5. The docs say supporting files ship with the skill. **Unverified** on claude.ai.
- Pins are read from the profile page through WebFetch. This worked from Claude Code. **Unverified** on claude.ai.
- `argument-hint` in each skill's frontmatter is Claude Code's field. Check that an upload with it syncs without error and that the skills still take their keywords. **Unverified** on claude.ai.
- The skill says GraphQL (`gh api graphql`, `gh repo view --json`) isn't available on claude.ai. **Unverified.** If it is available, read pins directly instead of from a summary of the profile page.

**Done when** each mode has run once on claude.ai, and anything that failed is fixed or written up here as its own item.

## 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

A scheduled task would save the stars, views, clones and top referrers of every public repo, once a week, to an artifact with a shared database, and chart the trend. The scorecard's outcomes panel could then link to it.

**Unverified**: that scheduled tasks and artifact databases are available where the plugin runs, and that the scheduled task gets the push access traffic needs.

**Done when** two weekly snapshots of every public repo are saved and charted on the page.

## 2. Timing

Nothing records how long a run takes or where the time goes. A full review clones the repo, makes many `gh api` calls, searches for similar repos and reads one profile per stargazer; triage makes several calls per fork. Measure before speeding anything up or adding a faster mode (item 4).

Have each mode record, at the start and end of every step, the time from the shell (`date -u +%s`) and the number of `gh api` calls made, and put them in the page's JSON as `timings`: a list of `{step, seconds, calls}`. The template shows them in a closed section at the foot of the page; overview and triage also give the totals. The times include Claude's own work between tool calls, which is what the user waits for, but can't separate it from time spent waiting on GitHub. A skill can't read its own token use.

**Unverified**: that the shell's clock on claude.ai runs on between tool calls, so the times are wall-clock.

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
- **README links that don't ship**: the README is in the zip, but its "Working on it" section links to `docs/`, which isn't. Move that section to `docs/README.md`, or have `scripts/package.sh` leave it out.
