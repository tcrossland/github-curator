# Backlog

Ideas for the plugin, grouped by the release they're meant for and in order within each group. Each says why it's worth doing and what done looks like; one with no other test is done when the change is made and the tests pass. Anything not yet checked against its source is marked **unverified**.

## Summary

| Item | Release | Kind | Size | Status |
|---|---|---|---|---|
| [Author identities](#author-identities) | 0.10.0 | Feature | S | todo |
| [Links between the pages](#links-between-the-pages) | Later | Pages | M | todo |
| [Launch drafts](#launch-drafts) | Later | New skill | M | todo |
| [Benchmark against good practice](#benchmark-against-good-practice) | Later | Scorecard panel | L | todo |
| [The GitHub connector on claude.ai](#the-github-connector-on-claudeai) | Later | Route | S | todo |
| [Traffic history](#traffic-history) | Waiting on time | New skill and scheduled task | M | in progress |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` when work starts. How to close an item is in the working agreement in [CLAUDE.md](../CLAUDE.md#working-agreement).

## Next

The next release, in the order to do it. An item's Release is the version it's meant for.

### Author identities

Let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. Triage's fork step reads each commit's author name and email domain from git, so the list would let it mark those commits as the user's.

**Done when** triage reads the list and marks matching commits as the user's.

## Later

Bigger features, in the order to do them.

### Links between the pages

Each scorecard, the quick review, the triage page, the portfolio page and Traffic history are separate artifacts found by title, and only the portfolio page links to scorecards. Quick and triage rows could link to a repo's scorecard when one exists, and a scorecard's header to the latest quick review, triage and portfolio page, from one listing of the user's artifacts. In Claude Code that listing can stop at the 50 most recently updated artifacts (`docs/github-facts.md`), so a page that finds no link for a page it names says one may exist, as a review's footer does.

**Done when** each page links to the others it names, and a template test covers each link.

### Launch drafts

When the review says publish or feature, draft the announcement: where it fits, and a post for each place, in the house style. It drafts only: posting is the user's call. It comes after Traffic history, which needs several weeks of referrers before it can show which places brought visitors.

**Done when**, for one repo recommended for featuring, it drafts posts for at least two places, each with the reason it fits (from the repo's referrers or where similar repos are discussed).

### Benchmark against good practice

The review checks the page, not the engineering. A visitor who opens `pyproject.toml` or the CI workflow judges the craft too, and nothing checks it today: the manifest, CI workflow and licence are read only to confirm facts on the page.

Add a **Practice** panel to the scorecard: a checklist of `done`, `todo` and `n/a`, each with its evidence, kept apart from the seven questions so it doesn't blur them. Its `todo` items join the fix prompt. It also feeds into Getting started, Tone and the feature call.

- **Common to every repo**: a README with what it is, how to install and run it, and the result; a licence (already checked under Getting started, so the panel only refers to that finding); tests, and CI that runs them on every push; a CI badge only when the badge is accurate; tagged releases and a changelog when it's versioned; CONTRIBUTING and issue templates only when it invites contributions. GitHub's community profile (`gh api repos/OWNER/REPO/community/profile`) reports most of the files and a health percentage.
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

### The GitHub connector on claude.ai

A claude.ai session's `gh` reads only the repos attached to it, so a first triage there attaches every fork to read its parent, one approval each past what Auto mode lets through. The claude.ai GitHub connector reads other owners' public repos without attaching them: by 2026-11-23 its repo tools answered on claude.ai (`docs/github-facts.md`, "The GitHub connector"). It can't see private repos, has none of stargazers, traffic, forks or pins, returns authors' email addresses and can write, so no skill uses it yet.

Decide whether a skill should read through it on claude.ai, and for which reads: forks' parents first. A skill that uses it keeps the email addresses out of everything it writes and calls none of its write tools.

**Done when** `docs/design.md` records the decision and its reason, and, if it's yes, a first triage on claude.ai reads its forks' parents through the connector, attaching fewer repos than it does today.

## Waiting on time

Started, and waiting on a date before it can close.

### Traffic history

The `traffic` skill and its weekly task have shipped. The task's first run on schedule, at 06:26 UTC on 2026-11-23, saved 15 of the 17 public repos: `github-curator` and the profile README repo weren't attached to the chat that created the task, and a run can't attach them. A snapshot of all 17 was saved by hand the same day. Whether the task itself now covers all 17 shows in its next run, early on 2026-11-30. If it doesn't, attach the two in a chat and run `traffic schedule` again.

**Done when** two weekly snapshots of every public repo are saved and charted on the page, the second by the weekly task on its schedule.
