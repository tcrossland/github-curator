# Backlog

Ideas for the plugin, grouped by the release they're meant for and in order within each group. Each says why it's worth doing and what done looks like; one with no other test is done when the change is made and the tests pass. Anything not yet checked against its source is marked **unverified**.

## Summary

| Item | Release | Kind | Size | Status |
|---|---|---|---|---|
| [Fewer approvals on claude.ai](#fewer-approvals-on-claudeai) | Next | Rule | S | todo |
| [6. Profile review](#6-profile-review) | Later | New skill | M | todo |
| [Links between the pages](#links-between-the-pages) | Later | Pages | M | todo |
| [10. Launch drafts](#10-launch-drafts) | Later | New skill | M | todo |
| [5. Benchmark against good practice](#5-benchmark-against-good-practice) | Later | Scorecard panel | L | todo |
| [Reviews side by side](#reviews-side-by-side) | Later | Rule | M | todo |
| [Author identities](#author-identities) | Later | Feature | S | todo |
| [GitHub's secret scanning on public repos](#githubs-secret-scanning-on-public-repos) | Later | Feature | S | todo |
| [1. Traffic history](#1-traffic-history) | Waiting on time | New skill and scheduled task | M | in progress |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` when work starts. When an item is done, delete its section and its summary row: the changelog and the commit that closes it record it. Keep a short section under Done only when an open item depends on what it found, such as figures, and keep only that part. Move an item between groups by moving its section and changing its row's Release.

## Next

### Fewer approvals on claude.ai

In Manual mode each `add_repo` call needs an approval, so attaching N repos takes N (`docs/github-facts.md`). Auto mode attached without a prompt in the 0.6.0-dev.3 check, but its check refused `add_repo` in some earlier chats, which is why attaching goes through Manual mode (`docs/design.md`). Trying Auto first and asking for Manual only after a refusal would save most approvals. Done when a claude.ai check shows how often Auto refuses, and the Attaching rule follows from it. The 0.8.0-dev.1 check on 2026-11-23 asked for read access by mistake, which attaches nothing on a public repo, so it measured nothing; the one push attach in that chat, made by `repo-review`, went through in Auto mode with no prompt. On 2026-11-23, on 0.8.0-dev.2, an Auto-mode chat attached five repos with push access, no refusals, after a request giving permission for each. With the 74 of 2026-11-21, Auto's only refusals are from 2026-11-20, so the Attaching rule can try Auto first and ask for Manual only after a refusal. Switching to Manual doesn't help WebFetch either: a link not from the conversation asks for approval in either mode (`docs/github-facts.md`). Done when `triage.md`, `portfolio.md` and `stargazers` attach in the chat's mode and suggest Manual only after a refusal.

## Later

Bigger features, in the order to do them.

### 6. Profile review

The profile page is the first thing a visitor sees. A profile README (the `OWNER/OWNER` repo), the bio, the pins and the featured repos aren't checked together today. On claude.ai it reads the profile page through WebFetch, so it depends on the item on WebFetch of GitHub pages there. `repo-review quick` leaves the profile README repo out for this skill, since Findable and Getting started don't apply to it.

A new skill, `profile-review`, would:
- check the bio and the pins, reusing the pin ranking from portfolio mode;
- draft a short profile README in the house style that introduces the featured repos, and names the contributions to other people's projects worth mentioning, from the `contributions` skill;
- publish a scorecard like the repo review's.

**Done when**, for a real profile, it produces:
- a pins recommendation that names what to pin and what to drop, with a reason for each;
- a draft profile README that links every recommended pin, and would read well to a visitor who has never heard of the user.

### Links between the pages

Each scorecard, the quick review, the triage page, the portfolio page and Traffic history are separate artifacts found by title, and only the portfolio page links to scorecards. Quick and triage rows could link to a repo's scorecard when one exists, and a scorecard's header to the latest quick review, triage and portfolio page, from one listing of the user's artifacts. Done when each page links to the others it names, and a template test covers each link.

### 10. Launch drafts

When the review says publish or feature, draft the announcement: where it fits, and a post for each place, in the house style. It drafts only: posting is the user's call. Traffic history (item 1) would show which places brought visitors before.

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

### Reviews side by side

`docs/design.md` has a portfolio run review its repos one at a time, since the request count is the account's and side-by-side reviews can't be told apart. Several repo URLs with no mode word now ask which mode to run, so they no longer start separate reviews at once, but a portfolio run whose reviews run in subagents still can. On 2026-11-21 one review ran alone, then seven ran in subagents four at a time: by their timing logs they took 2,312 s between them and the last finished 817 s after the first began. Three things came up that the skill doesn't cover. Each review's `calls` included the others' requests, and the page has no field to say so, so each footer said it in a sentence the subagents were given. The reviews share the search limit of 30 a minute (`gh api rate_limit`); none was refused, and the retry after a minute that the subagents were told to use isn't in the skill. And nothing says how many may run at once. Done when the skill either rules side-by-side reviews out, or says how to run them (how many at once, what to do when a search is refused) and the page shows when a review's counts include other runs'.

### Author identities

Let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. Triage's fork step now reads each commit's author name and email domain from git, so the list would let it mark those commits as the user's. Done when triage reads the list and marks matching commits as the user's.

### GitHub's secret scanning on public repos

GitHub's own secret scanning is free on public repos but off until the owner turns it on: with it off, `repos/OWNER/REPO/secret-scanning/alerts` gives HTTP 404 "Secret scanning is disabled on this repository" (seen 2026-11-21, **unverified** as a rule until it's in `docs/github-facts.md` with its source). For a public repo the review recommends keeping or archiving, it could read the alerts, and recommend turning scanning and push protection on when they're off. It can't replace betterleaks before publishing: GitHub's docs give secret scanning on user-owned private repos only on its enterprise plans, and on a public repo it runs only once the code is out. The GitHub MCP's `run_secret_scanning` scans snippets or diffs rather than history, and sends them to GitHub, which is why a hosted scanner was ruled out before. Done when the facts are recorded with their sources, the review reads the alerts for a public repo and recommends turning scanning on when it's off, and a test covers the 404.

## Waiting on time

Started, and waiting on a date before it can close.

### 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

The `traffic` skill saves a snapshot of every public repo's stars, forks, daily views and clones and top referrers as one document in the database of a page titled "Traffic history", which charts them across snapshots, and `schedule` sets up a weekly task that runs it. The page exists, holding the hand snapshot of 2026-11-20 and one taken with the skill's script in Claude Code on 2026-11-21.

A claude.ai chat attached all 74 public repos in Auto mode and created the weekly task, which runs early on Mondays, and a run of it started by hand saved a snapshot of all 74 (`docs/github-facts.md`). The page holds four snapshots, three of them from 2026-11-21.

The review's Outcomes panel links to the page.

The first run on schedule saved a snapshot on its own at 06:26 UTC on 2026-11-23, of 15 of the 17 public repos the account now has: `github-curator` and the profile README repo weren't attached to the chat that created the task, and a run can't attach them. What's left is attaching those two in a chat and running `traffic schedule` again, so the next run covers every public repo.

**Done when** two weekly snapshots of every public repo are saved and charted on the page, the second by the weekly task on its schedule.
