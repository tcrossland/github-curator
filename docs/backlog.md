# Backlog

Ideas for the plugin, in the order to do them. Each says why it's worth doing and what done looks like. Anything not yet checked against its source is marked **unverified**.

## Summary

| # | Item | Kind | Size | Depends on | Status |
|---|---|---|---|---|---|
| 11 | [GitHub access from a claude.ai session](#11-github-access-from-a-claudeai-session) | Fix | M | none | todo |
| 1 | [Traffic history](#1-traffic-history) | New skill and scheduled task | M | none | todo |
| 4 | [Quick review](#4-quick-review) | New mode | M | none | todo |
| 5 | [Benchmark against good practice](#5-benchmark-against-good-practice) | Scorecard panel | L | none | todo |
| 6 | [Profile review](#6-profile-review) | New skill | M | none | todo |
| 10 | [Launch drafts](#10-launch-drafts) | New skill | M | 1 helps | todo |
| 8 | [Forks](#8-forks) | New skill | M | none | todo |
| 9 | [Secrets scanner for publishing](#9-secrets-scanner-for-publishing) | Checklist tool | M | none | todo |
| – | [Other smaller items](#smaller) | Fixes | S each | none | any time |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` when work starts. When an item is done, delete its section and its summary row, and take it out of other items' Depends on: the changelog and the commit that closes it record it. Keep a short section under Done only when an open item depends on what it found, such as figures, and keep only that part. A smaller item is simply deleted.

## 11. GitHub access from a claude.ai session

The 0.2.4 test runs on claude.ai showed that the session's `gh` is bound to the repos attached to it. GraphQL, `user/repos`, every `users/…` and `orgs/…` path, and `repos/OWNER/REPO` for any repo not attached are all refused with HTTP 403. The facts are in `docs/github-facts.md`. What each mode lost:
- **Triage** listed its repos through `list_repos` and took their fields from the search API, but couldn't read a README or compare a fork with its parent, so it marked no repo clear. On claude.ai it's a list, not a triage.
- **Stargazers** listed the stargazers but couldn't read a single profile, so it couldn't pick the ones worth a look, in the skill or in the review's Outcomes panel.
- **Similar repos** described each repo from its search result, because other owners' READMEs were refused.

Three more probes tested the routes around this (facts in `docs/github-facts.md`). What they settled:
- **Attaching works only with push access, and only with the user's permission.** Read access gives an anonymous git clone and nothing more. With the user's permission one chat attached all 74 of the user's public repos with push access, and an attached fork's `.parent` can be read. In auto mode, push access is refused unless the user asked for it, and even then not reliably: on 2026-11-20 two chats whose request gave permission had every `add_repo` refused. So any step that attaches a repo needs a fallback for when it can't.
- **Cross-fork compare is out**, even for an attached fork: the proxy refuses it with HTTP 400.
- **Git works** for any public repo without attaching it, through the session's proxy as in Claude Code: a sparse clone of just the README, and a fork's count beyond its parent from treeless clones.
- **WebFetch isn't a source of exact text**: it reworded and cut a README, and was rate-limited on repo pages. A profile through it gives the name, followers and pinned repos only.
- **Issue search answers**, so the user's merged pull requests to a parent can still be read.

The route, the same in both places where it can be:
- **READMEs** (triage's own repos, similar repos): a sparse clone that checks out only the README.
- **A fork against its parent**: the count and the authors from treeless clones, `git rev-list --count` and `git log`. This also lifts the compare API's limit of 250 commits. A parent as large as elixir's still costs its whole commit history.
- **A fork's parent**: only `gh api repos/OWNER/FORK` gives it, which on claude.ai needs the fork attached with push access; `list_repos`, search and GraphQL don't (a third probe checked all three). A parent doesn't change, so the triage page records each fork's parent and its default branch, and a later triage reads them from the previous page, as it already reads that page to compare. Only forks new since then need the API. The first triage on claude.ai either attaches every fork, with the user's permission, or is run from Claude Code instead, where the user's own `gh` reads every parent; the page says which.
- **Pull requests to the parent**: issue search, as now.
- **Stargazers' profiles**: WebFetch of `github.com/LOGIN`, one at a time, judging the field from the pinned repos' descriptions, labelled "profile page summary". Say in the reply which of bio, company and location weren't available: the profile tried had none, so whether WebFetch gives them is untested.
- **Private repos** need attaching too.
- **On claude.ai, triage asks once for permission to attach** the forks whose parent it doesn't know yet and the private repos, and leaves any it can't attach as `review`, saying which and why.

A first triage on claude.ai with no previous page to read parents from has to attach every fork and private repo (61 forks and 11 private repos on this account). One chat has attached 74 public repos; whether private repos attach the same way is **unverified**.

Two smaller items are part of this one, since they change the same steps:
- **Stargazers when profiles can't be read**: neither skill says what to do when Step 2 of `stargazers` can't read the profiles, so the scorecard falls back to "None in the same field", which reads as a judgement that was never made (seen in the 0.2.4 test runs, where every profile call was refused). Say "Not available" with the reason instead, in the `stargazers` reply and in the review's Stargazers lists. Done when both skills say so, and a template test checks the scorecard's wording.
- **Rate limits in triage**: the pull-request search goes through GitHub's search API, whose rate limit is far lower than the rest of the API's, so an account with many forks that have commits could hit it. Say in Step 8 to pace the searches and to note any that were refused. Done when triage on an account with more than 30 such forks completes.

**Done when** triage on claude.ai marks the clear deletes it marks in Claude Code on the same account, stargazers there reads profiles or says plainly that it can't, and a triage with the timing log (item 2) shows per-step times on its page, with its slowest step written up here. The new route's clones are the cost to watch: a parent as large as elixir's costs its whole commit history.

## 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

A scheduled task would save the stars, views, clones and top referrers of every public repo, once a week, to an artifact with a shared database, and chart the trend. The scorecard's outcomes panel could then link to it.

A claude.ai chat has scheduled tasks and artifact databases, its `gh` reads traffic once a repo is attached with push access, and a scheduled run gets the repos attached in the chat that created its task, traffic included (`docs/github-facts.md`). So the task is created from a chat that has attached every public repo. One chat has attached all 74 public repos with push access and read traffic for every one. **Unverified**: that each run of a recurring task, started on schedule, keeps the repos (the one run that read traffic was started by hand; an hourly check task is due to show it). If that fails, the fallback is a scheduled task in the Claude Code desktop app, which runs on the user's computer with their own `gh`.

Until this lands, a snapshot of every public repo is saved by hand once a week to a gitignored file. The first was saved on 2026-11-20, for 74 repos, forks included: stars, forks, the daily views and clones GitHub still holds, and top referrers, so snapshots can be merged by repo and day and loaded into the page's database once it exists.

**Done when** two weekly snapshots of every public repo are saved and charted on the page.

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
- draft a short profile README in the house style that introduces the featured repos, and names the contributions to other people's projects worth mentioning, from the `contributions` skill;
- publish a scorecard like the repo review's.

**Done when**, for a real profile, it produces:
- a pins recommendation that names what to pin and what to drop, with a reason for each;
- a draft profile README that links every recommended pin, and would read well to a visitor who has never heard of the user.

## 10. Launch drafts

When the review says publish or feature, draft the announcement: where it fits, and a post for each place, in the house style. It drafts only: posting is the user's call. Traffic history (item 1) would show which places brought visitors before.

**Done when**, for one repo recommended for featuring, it drafts posts for at least two places, each with the reason it fits (from the repo's referrers or where similar repos are discussed).

## 8. Forks

A fork with commits says more than a star: someone used the code. This would be the `stargazers` skill's counterpart. It would list the forks that have commits beyond the user's repo, what they changed and who changed it. Its rules would match: public data only, never contact anyone. It would also tell triage how much others rely on a repo.

**Done when** it runs on a repo with forks, lists each fork's commits beyond the original with their authors, and is called from the repo review's outcomes panel.

## 9. Secrets scanner for publishing

The secrets check before publishing relies on the model reading `git log`, which is weak over a long history. Use a dedicated scanner instead. Candidates, each licence read from the project's own LICENSE file on 2026-11-20:
- gitleaks, MIT;
- trufflehog, AGPL-3.0.

AGPL is copyleft, so gitleaks is the one to use. Calling a tool installed on the machine is different from bundling it.

**Done when** the before-publishing check runs a scanner over the full history and reports each finding with its commit and file, and a test repo with a planted fake key is caught.

## Smaller

Each is done when the change is made and the tests pass, unless it says otherwise. They can be done at any time.

- **Check `contributions` on claude.ai**: it was run only in Claude Code. In a claude.ai session, `gh api user` and `user/memberships/orgs` may be refused as unscoped paths, and the skill then takes the user's organisations from `list_repos`. Done when a claude.ai run gives the same three groups and counts as Claude Code on the same account, or says plainly which part it couldn't read, and the result is in `docs/github-facts.md`.
- **Author identities**: let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. It changes triage's fork step, which item 11 is rewriting, so it waits for that. Done when triage reads the list and marks matching commits as the user's.
- **Fix prompts on the overview**: the overview page links each repo's scorecard but has no fix prompt, so acting on an overview means opening each scorecard in turn. Add a copy button to each row that has failing or flagged questions, copying that repo's fix prompt as its scorecard builds it (`fixPrompt` with every item). Keep one prompt per repo, not one for all of them: each runs in its own Claude Code session in that repo. Done when the overview's JSON carries each repo's `fixPrompt`, each row's button copies the same text as its scorecard's "All", and a template test checks it.
- **Test uploads between releases**: changes now collect under Unreleased, and `version` changes only when a release is cut, but trying a change on claude.ai still needs an upload. Both claude.ai's replace prompt and the install skill's sync check go by version, so a test zip with the last release's version can't be told apart once synced. A `--dev` flag on `scripts/package.sh` could stamp a pre-release version such as `0.2.15-dev.1` into the zip's manifest, leaving the committed one alone. Whether claude.ai accepts a pre-release version in `plugin.json` is **unverified**. Done when one test upload with a pre-release version is seen to install and sync, the result is in `docs/github-facts.md`, and the flag is added (or, if it's refused, the README says how to test a change instead).
- **Check the Claude Code tool list**: 0.2.14 added a list near the top of `repo-review`'s `SKILL.md` saying what Claude Code uses in place of each claude.ai tool, and what a run does with no artifact tool. Whether Claude Code outside the desktop app has an artifact tool is **unverified**. Done when a review run in a Claude Code session started on 0.2.14 or later finds the previous scorecard by following the list, and the result is in `docs/github-facts.md`.

## Done

What finished items found that open items still use.

### 2. Timing

Item 4 measures against these figures. Every page's Timings section gives each step's seconds and GitHub calls, logged as `docs/design.md` describes. The times include Claude's own work between tool calls, which can't be told apart from waiting on GitHub.

**Figures**, all in Claude Code:
- Timed by hand in the 0.2.4 test runs, before the log: a review of spacy-annotator about 310 s, an overview of two repos about 236 s, triage 105 s and stargazers 31 s.
- One review logged on 0.2.5: 228 s, slowest the seven questions (89 s).
- A cold overview of stat-arb-from-scratch and claude-code-methodology on 0.2.8, on 2026-11-20, in a fresh session with `no-publish`: 341 s. The overview's rows give 171 s and 134 s for the two reviews and 36 s for its own page. Two earlier overviews that day don't count: one ran its reviews interleaved, and a re-run on 0.2.7 reused judgements made earlier in its session, giving 52 s and 44 s per repo. Set against that re-run, about 120 s and 90 s of each cold review was judging.

The cold reviews' rows, as seconds, counted calls and searches:

| Step | stat-arb-from-scratch | claude-code-methodology |
|---|---|---|
| Get the draft | 35 s, 3 calls | 51 s, 3 calls |
| Outcomes | 4 s, 3 calls | 5 s, 3 calls |
| Similar repos | 21 s, 0 calls, 5 searches | 18 s, 0 calls, 4 searches |
| Questions | 50 s, 1 call | 21 s, not read |
| Compare | 19 s, 0 calls | 35 s, not read |
| Verify and recommend | 33 s, 1 call | 1 s, not read |
| Build | 8 s, 0 calls | 1 s, 0 calls |
| Total | 170 s, 8 calls | 132 s, 6 calls |

Each review also made 4 traffic requests and read the pins through GraphQL, none of which `core.used` counts. GitHub's share is small: Outcomes took 4 or 5 s, and the searches about 20 s.

Two things limit how far the rows can be read:
- **Step boundaries.** A step's line is stamped when the command that writes it runs, so whatever Claude thinks and writes before that command counts to the step it closes. Where one command wrote a step's line and then did the next step's work, that work went to the earlier step: claude-code-methodology's Compare (35 s) includes writing the whole page's JSON, which leaves 1 s each for Verify and recommend and for Build. So the split between neighbouring steps is uncertain by tens of seconds, while each review's total holds. Since 0.2.10 each step's line has a command of its own.
- **Unread calls.** Three of claude-code-methodology's rows have no call count because the rate limit's reads were inconsistent. On 0.2.9 only the two rows either side of the stray read would lack one. Its total of 6 comes from its first and last lines.

**Slowest steps, as candidates to speed up**:
- **Review: the seven questions.** 89 s in the 0.2.5 review and 50 s in stat-arb-from-scratch's, the slowest step in both, and judging is most of the gap between the cold and the warm overview. Item 4's quick review answers three of the questions from the API and the README alone.
- **Review: getting the draft.** 35 s and 51 s, the slowest step in claude-code-methodology's review. Besides the clone and the files, it reads the previous scorecard, whose whole page comes back through the artifact read (this run's saved scorecards are about 46 KB each) for the one JSON block that Step 3 compares with. Whether the read can return less is **unverified**.
- **Overview: the reviews.** The first review, 171 s, is its slowest row, and the reviews take 305 of its 341 s. An overview gets faster only as a review does, or, for many repos, through item 4.
