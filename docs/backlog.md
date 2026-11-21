# Backlog

Ideas for the plugin, in the order to do them. Each says why it's worth doing and what done looks like. Anything not yet checked against its source is marked **unverified**.

## Summary

| # | Item | Kind | Size | Depends on | Status |
|---|---|---|---|---|---|
| 11 | [GitHub access from a claude.ai session](#11-github-access-from-a-claudeai-session) | Fix | M | none | in progress: to check on claude.ai |
| 1 | [Traffic history](#1-traffic-history) | New skill and scheduled task | M | none | todo |
| 4 | [Quick review](#4-quick-review) | New mode | M | none | todo |
| 5 | [Benchmark against good practice](#5-benchmark-against-good-practice) | Scorecard panel | L | none | todo |
| 6 | [Profile review](#6-profile-review) | New skill | M | none | todo |
| 10 | [Launch drafts](#10-launch-drafts) | New skill | M | 1 helps | todo |
| 8 | [Forks](#8-forks) | New skill | M | none | todo |
| – | [Other smaller items](#smaller) | Fixes | S each | none | any time |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` when work starts. When an item is done, delete its section and its summary row, and take it out of other items' Depends on: the changelog and the commit that closes it record it. Keep a short section under Done only when an open item depends on what it found, such as figures, and keep only that part. A smaller item is simply deleted.

## 11. GitHub access from a claude.ai session

On claude.ai the session's `gh` goes through a proxy bound to the repos attached to the session: GraphQL, `user/repos`, every `users/…` and `orgs/…` path and any repo not attached are refused with HTTP 403, and compare across forks with 400 (details in `docs/github-facts.md`). In the 0.2.4 test runs that left triage a list that marked no repo clear, stargazers unable to read a single profile, and similar repos described from search results alone.

The skills now take routes that work there too, the same in Claude Code where they can be (the reasons are in `docs/design.md`, under Routes that work on claude.ai too):
- READMEs from a clone that checks out only the README.
- A fork's commits beyond its parent from a treeless clone of the fork with the parent's default branch fetched into it. In Claude Code its count matched the compare API's for all 61 of this account's forks.
- A fork's parent recorded on the triage page and read from there by the next triage, so only forks new since need attaching.
- On claude.ai, the listing's fields from one repository search, and attaching through Manual mode, asked for once, with any repo not attached sent to review.
- The user's pull requests to the parents from one search, 100 a page, rather than one search per fork, so the search API's 30 a minute isn't reached (this replaces pacing the searches).
- Stargazers' profiles from the profile page by WebFetch when `users/LOGIN` is refused, labelled "profile page summary", and "Not available" with the reason, in the reply and the review's Stargazers lists, when no profile could be read.
- An organisation's triage on claude.ai stops and says to run it from Claude Code.

What only a claude.ai run, on an upload that has these changes, can check:
- **A first triage**: it asks to switch to Manual mode, attaches every fork and private repo (61 and 11 on this account), and runs the git commands in the VM. **Unverified**: whether Manual mode's prompt for `add_repo` can be allowed for the rest of the chat; if it can't, that's 72 approvals, and a first triage is better run from Claude Code.
- **A second triage**: it reads each fork's parent from the first page and attaches only the private repos and any new forks.
- **The same calls**: it marks the clear deletes Claude Code marks on the same account.
- **Search on claude.ai**: whether `search/repositories?q=user:LOGIN+fork:true` includes private repos there (**unverified**; triage reads private repos from the API once attached, either way), and the pull-request search's 320 results on this account.
- **A private repo's README** from the sparse clone once it's attached (`git ls-remote` answered after attaching, but no clone has been tried).
- **Stargazers**: the stargazer list for an attached repo (**unverified** on claude.ai), and whether WebFetch of a profile page gives the bio, company, location and the pinned repos' descriptions when a profile has them.
- **Timings**: the triage page's per-step times, `Attach` included, with its slowest step written up here.

**Done when** triage on claude.ai marks the clear deletes it marks in Claude Code on the same account, stargazers there reads profiles or says plainly that it can't, and a triage's page shows per-step times from item 2's log, with its slowest step written up here.

## 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

A scheduled task would save the stars, views, clones and top referrers of every public repo, once a week, to an artifact with a shared database, and chart the trend. The scorecard's outcomes panel could then link to it.

A claude.ai chat has scheduled tasks and artifact databases, its `gh` reads traffic once a repo is attached with push access, and a scheduled run gets the repos attached in the chat that created its task, traffic included (`docs/github-facts.md`). So the task is created from a chat that has attached every public repo. One chat has attached all 74 public repos with push access and read traffic for every one. A recurring task's runs on schedule got all 74 too, including one after the chat that created it was deleted, so the chat needn't be kept. A scheduled task in the Claude Code desktop app, which runs on the user's computer with their own `gh`, stays the fallback if a claude.ai task stops working.

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

## Smaller

Each is done when the change is made and the tests pass, unless it says otherwise. They can be done at any time.

- **`contributions` on claude.ai**: its commands, run in a claude.ai chat on 2026-11-21, don't give Claude Code's groups (details in `docs/github-facts.md`). `gh api user` answers, but `user/memberships/orgs` is refused, and the fallback, the owners `list_repos` gives, missed one of the user's organisations and added a user account. The private search also found 1 pull request where Claude Code finds 2. The skill now says both in its reply on claude.ai. Done when a claude.ai run of the skill, on an upload that has it, shows both.
- **Secrets scan on claude.ai**: `repo-review` now fetches betterleaks 1.10.1 into the claude.ai VM, checked against the release's checksums, but no review on claude.ai has run it yet. Done when a review of a private repo on claude.ai, on an upload that has the fetch, runs the scan and its page says so.
- **Draft reply holds steady**: `other-people`'s `draft-reply` passed 9 of 11 runs on 2026-11-20; the two misses weren't traced. Done when `scripts/evals.sh --case other-people --ablation none --runs 10 --keep-temp` passes every run, or each miss's trace says why and the rule or grader is fixed.
- **Author identities**: let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. Triage's fork step now reads each commit's author name and email domain from git, so the list would let it mark those commits as the user's. Done when triage reads the list and marks matching commits as the user's.
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
