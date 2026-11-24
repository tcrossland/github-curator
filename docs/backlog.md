# Backlog

Ideas for the plugin, grouped by the release they're meant for and in order within each group. Each says why it's worth doing and what done looks like; one with no other test is done when the change is made and the tests pass. Anything not yet checked against its source is marked **unverified**.

## Summary

| Item | Release | Kind | Size | Status |
|---|---|---|---|---|
| [Profile review: rules from its first runs](#profile-review-rules-from-its-first-runs) | 0.9.0 | Rule | S | todo |
| [Reviews side by side](#reviews-side-by-side) | 0.10.0 | Rule | M | todo |
| [Author identities](#author-identities) | 0.10.0 | Feature | S | todo |
| [Links between the pages](#links-between-the-pages) | Later | Pages | M | todo |
| [10. Launch drafts](#10-launch-drafts) | Later | New skill | M | todo |
| [5. Benchmark against good practice](#5-benchmark-against-good-practice) | Later | Scorecard panel | L | todo |
| [1. Traffic history](#1-traffic-history) | Waiting on time | New skill and scheduled task | M | in progress |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` when work starts. When an item is done, delete its section and its summary row: the changelog and the commit that closes it record it. Keep a short section under Done only when an open item depends on what it found, such as figures, and keep only that part. Move an item between groups by moving its section and changing its row's Release.

## Next

The next two releases, in the order to do them. An item's Release is the version it's meant for.

### Profile review: rules from its first runs

`repo-review profile` ran on a real profile on 2026-11-24, in Claude Code and on claude.ai, and met its done-when in both. The runs raised five questions its rules don't settle:
- **Employers from the bio.** Both runs counted an employer the bio names, which the `contributions` rules don't do. `user.json` already holds `company`, which could be passed as an employer and named in the footer, or the rule could forbid it.
- **Pins quoted as one line.** The Claude Code run quoted six pin names as one line, labelled "summarised, not a verbatim line". `profile.md` could ask for one pin name per quote.
- **A draft that puts back what the user removed.** The claude.ai run's draft named three contributions, though the previous review noted the user had removed that list, and left the call to the user. A re-run could keep out of the draft whatever the user took out of the README since the previous draft.
- **Pins whose state is unknown.** On claude.ai, two recommended pins the page summary didn't name came out as "pin (check whether it's already pinned)". The changes have no `check` kind for that.
- **The bio from the page summary.** By the claude.ai chat's account, the profile page summary gave the status message as the bio (**unverified**). `user` gave the bio there, so the fallback is rare, but it could say to take the bio only from a line the summary labels as the bio.

Done when each is a rule in `profile.md`, with a test or an eval case where it can have one, or is recorded in `docs/design.md` as decided against.

### Reviews side by side

`docs/design.md` has a portfolio run review its repos one at a time, since the request count is the account's and side-by-side reviews can't be told apart. Several repo URLs with no mode word now ask which mode to run, so they no longer start separate reviews at once, but a portfolio run whose reviews run in subagents still can. On 2026-11-21 one review ran alone, then seven ran in subagents four at a time: by their timing logs they took 2,312 s between them and the last finished 817 s after the first began. Three things came up that the skill doesn't cover. Each review's `calls` included the others' requests, and the page has no field to say so, so each footer said it in a sentence the subagents were given. The reviews share the search limit of 30 a minute (`gh api rate_limit`); none was refused, and the retry after a minute that the subagents were told to use isn't in the skill. And nothing says how many may run at once. Settle it before the next large portfolio run. If the skill rules them out, the change is a fix and can go in a patch release. Done when the skill either rules side-by-side reviews out, or says how to run them (how many at once, what to do when a search is refused) and the page shows when a review's counts include other runs'.

### Author identities

Let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. Triage's fork step now reads each commit's author name and email domain from git, so the list would let it mark those commits as the user's. Done when triage reads the list and marks matching commits as the user's.

## Later

Bigger features, in the order to do them.

### Links between the pages

Each scorecard, the quick review, the triage page, the portfolio page and Traffic history are separate artifacts found by title, and only the portfolio page links to scorecards. Quick and triage rows could link to a repo's scorecard when one exists, and a scorecard's header to the latest quick review, triage and portfolio page, from one listing of the user's artifacts. In Claude Code that listing can stop at the 50 most recently updated artifacts (`docs/github-facts.md`), so a page that finds no link for a page it names says one may exist, as a review's footer does. Done when each page links to the others it names, and a template test covers each link.

### 10. Launch drafts

When the review says publish or feature, draft the announcement: where it fits, and a post for each place, in the house style. It drafts only: posting is the user's call. It comes after Traffic history (item 1), which needs several weeks of referrers before it can show which places brought visitors.

**Done when**, for one repo recommended for featuring, it drafts posts for at least two places, each with the reason it fits (from the repo's referrers or where similar repos are discussed).

### 5. Benchmark against good practice

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

## Waiting on time

Started, and waiting on a date before it can close.

### 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

The `traffic` skill saves a snapshot of every public repo's stars, forks, daily views and clones and top referrers as one document in the database of a page titled "Traffic history", which charts them across snapshots, and `schedule` sets up a weekly task that runs it, early on Mondays. The review's Outcomes panel links to the page.

The task's first run on schedule saved a snapshot on its own at 06:26 UTC on 2026-11-23, of 15 of the 17 public repos the account has: `github-curator` and the profile README repo weren't attached to the chat that created the task, and a run can't attach them. A snapshot of all 17 was saved at 13:15 UTC the same day, outside the schedule. Whether the task itself now covers all 17 shows in its next run, early on 2026-11-30. If it doesn't, attach the two in a chat and run `traffic schedule` again.

**Done when** two weekly snapshots of every public repo are saved and charted on the page, the second by the weekly task on its schedule.
