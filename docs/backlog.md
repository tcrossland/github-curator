# Backlog

Ideas for the plugin, in the order to do them. Each says why it's worth doing and what done looks like. Anything not yet checked against its source is marked **unverified**.

## Summary

| # | Item | Kind | Size | Depends on | Status |
|---|---|---|---|---|---|
| 2 | [Timing](#2-timing) | Measurement | S | 0, 11 for triage on claude.ai | in progress |
| 14 | [Save traffic until item 1 lands](#14-save-traffic-until-item-1-lands) | Stopgap and check | S | none | todo |
| 3 | [Split `SKILL.md` by mode](#3-split-skillmd-by-mode) | Restructure | S | 0 | todo |
| 11 | [GitHub access from a claude.ai session](#11-github-access-from-a-claudeai-session) | Fix | M | 3 | todo |
| 7 | [Behaviour evals](#7-behaviour-evals) | Tests | M | 3 | todo |
| 1 | [Traffic history](#1-traffic-history) | New skill and scheduled task | M | 14 | todo |
| 4 | [Quick review](#4-quick-review) | New mode | M | 2, 3 | todo |
| 12 | [Other people in the review](#12-other-people-in-the-review) | Scorecard panel and checks | M | 7 helps | todo |
| 5 | [Benchmark against good practice](#5-benchmark-against-good-practice) | Scorecard panel | L | 3, 7 helps | todo |
| 13 | [Contributions to other people's projects](#13-contributions-to-other-peoples-projects) | New skill | M | none | todo |
| 6 | [Profile review](#6-profile-review) | New skill | M | 13 helps | todo |
| 10 | [Launch drafts](#10-launch-drafts) | New skill | M | 1 helps | todo |
| 8 | [Forks](#8-forks) | New skill | M | none | todo |
| 9 | [Secrets scanner for publishing](#9-secrets-scanner-for-publishing) | Checklist tool | M | none | todo |
| – | [Other smaller items](#smaller) | Fixes | S each | none | any time |
| – | [Reply counts from the JSON](#reply-counts-from-the-json) | Fix | S | none | done |
| 0 | [Prove the current version on claude.ai](#done) | Check | S | none | done |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` or `done` as work moves, and move a done item's section to the end, or delete it once the summary row says enough.

## 2. Timing

Nothing records how long a run takes or where the time goes. A full review clones the repo, makes many `gh api` calls, searches for similar repos and reads one profile per stargazer; triage makes several calls per fork. Measure before speeding anything up or adding a faster mode (item 4).

Have each mode record, at the start and end of every step, the time from the shell (`date -u +%s`) and the number of `gh api` calls made, and put them in the page's JSON as `timings`: a list of `{step, seconds, calls}`. The template shows them in a closed section at the foot of the page; overview and triage also give the totals. The times include Claude's own work between tool calls, which is what the user waits for, but can't separate it from time spent waiting on GitHub. A skill can't read its own token use.

The shell's clock on claude.ai is wall-clock (`docs/github-facts.md`).

**First figures**, timed by hand in the 0.2.4 test runs, before the skill logged anything (runs 1 and 2 rebuilt from file and publish times, to about ±10 seconds): about 682 s across the four runs. In every run the time went to Claude's own work between calls, not to waiting on GitHub:
- review of spacy-annotator: about 310 s, slowest building the run and checking its quotes and numbers (Steps 3 and 4, about 95 s);
- overview of two repos: about 236 s, slowest Step 1 and Steps 2 to 4, about 70 s each;
- triage: 105 s, slowest the signals (37 s), though most of its reads were refused (item 11);
- stargazers: 31 s, slowest reading profiles (12 s), all refused.

**Status**: the skill and template side is in. `SKILL.md` has a Timing section: each step appends its name, `date -u +%s` and the rate limit's `core.used` to a log, and a script turns the log into `timings`, with `calls` read from the rate limit (which costs no request) rather than counted by hand. Search requests aren't in `core.used`, so they're counted by hand as `searches`. The template shows the rows and a total in a closed section above the footer, in all three modes. It shipped in 0.2.5 (2026-11-19). One review has been logged so far, in Claude Code, and its slowest step was the seven questions. Still to do: an overview with the log on claude.ai with 0.2.5, and a triage. Time the triage in Claude Code, or on claude.ai once item 11 is done: on claude.ai today most of triage's reads are refused, so its times would describe a run that skipped most of its work (105 s in the 0.2.4 test). `gh api rate_limit` answers on claude.ai and counts calls there; its count is shared with anything else using the account at the same time (`docs/github-facts.md`).

**Done when** a review, an overview and a triage each show per-step times on their pages, and the slowest step of each is written up here, as a candidate to speed up.

## 14. Save traffic until item 1 lands

GitHub drops traffic after 14 days, and item 1 waits on three unverified points, so it won't land soon. Until it does:
- save each public repo's views, clones and top referrers once a week, by hand, to a gitignored file;
- check on claude.ai whether scheduled tasks and artifact databases are available there, and whether a scheduled task gets the push access traffic needs, and record each in `docs/github-facts.md`.

The smaller item on the traffic claim goes with it:
- **Recheck the traffic claim**: `docs/github-facts.md` marks "14 days, needs push access" as not rechecked. Done when it has a source and a date.

**Done when** the first snapshot is saved, and item 1's three unverified points and the traffic claim each have a source and a date in `docs/github-facts.md`.

## 3. Split `SKILL.md` by mode

`skills/repo-review/SKILL.md` is 360 lines (49 KB), and every run loads all of it, including the overview and triage steps that a single review never uses. Move Step 7 (overview) and Step 8 (triage) into supporting files beside it, linked from the modes list and read only in those modes. They're only the last 60 or so lines, so a single review saves about a sixth of the file today. The larger gain is keeping item 11's changes to triage, and whatever later items add, out of every review. Item 11 rewrites Step 8 and item 5 would add more to the file, so do this before both.

The smaller item on the quote checker goes with it, since both move code out of `SKILL.md` and both change what the tests read:
- **Quote checker as a file**: move the quote checker from `SKILL.md` into `skills/repo-review/verify_run.py`, so it's run rather than retyped, and point `tests/test_verify_run.py` at the new file.

**Done when** a single review loads only the shared rules and Steps 1 to 6, the overview and triage files are linked by relative path, the quote checker runs from `verify_run.py`, and the tests still pass.

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

Two smaller items are part of this one, since they change the same steps:
- **Stargazers when profiles can't be read**: neither skill says what to do when Step 2 of `stargazers` can't read the profiles, so the scorecard falls back to "None in the same field", which reads as a judgement that was never made (seen in the 0.2.4 test runs, where every profile call was refused). Say "Not available" with the reason instead, in the `stargazers` reply and in the review's Stargazers lists. Done when both skills say so, and a template test checks the scorecard's wording.
- **Rate limits in triage**: the pull-request search goes through GitHub's search API, whose rate limit is far lower than the rest of the API's, so an account with many forks that have commits could hit it. Say in Step 8 to pace the searches and to note any that were refused. Done when triage on an account with more than 30 such forks completes.

**Done when** triage on claude.ai marks the clear deletes it marks in Claude Code on the same account, and stargazers there reads profiles or says plainly that it can't.

## 7. Behaviour evals

The tests cover code (the quote checker and the template), not the skill's judgement. A change to a rule could flip a recommendation without anything noticing. Keep a few known cases, each with the input and the expected call:
- an unchanged fork nobody uses is a clear delete in triage;
- a fork with commits beyond its parent is never clear;
- a private repo never fails Findable on visibility alone;
- an archived repo with every item done is recommended archive, with nothing to do.
- the same commit gets the same statuses twice. In the 0.2.4 test runs, claude-code-methodology's Way in was flagged in one review and passed in the next, on the same commit, so a case that runs one repo twice would catch a rule that leaves too much to judgement.

Do this before items 12 and 5, which change rules.

Claude Code has a `claude plugin eval` command that reads cases from `evals/` by default. **Unverified**: how its cases and checks are written.

**Done when** the cases above run with one command, and each fails if its rule is removed from `SKILL.md`.

## 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

A scheduled task would save the stars, views, clones and top referrers of every public repo, once a week, to an artifact with a shared database, and chart the trend. The scorecard's outcomes panel could then link to it.

**Unverified**: that scheduled tasks and artifact databases are available where the plugin runs, and that the scheduled task gets the push access traffic needs. Item 14 settles these and saves the data by hand until this item lands.

**Done when** two weekly snapshots of every public repo are saved and charted on the page.

## 4. Quick review

A `quick` mode that reads only the API and the README, with no clone, quote checker, stargazers or search for similar repos, and answers the questions those can settle: Hook (the description and the README's opening), Findable (description and topics) and Way in (a licence, and whether the README says how to run it). It gives each repo a row of statuses and signals, not a page of its own, and its results are provisional, as triage's are.

Uses:
- **Similar repos** in a full review: a quick review of each says what it does better than the repo under review (a clearer opening, the topics people search for), where today the panel has only their descriptions.
- **Triage's repos to review**: rank them by a quick pass before spending full reviews on them.
- **Overview of many repos**, when a full review of each would take too long.

**Done when** a quick review of ten repos takes a small part of the time an overview of the same ten takes (from item 2's timings), and its Hook, Findable and Way in statuses agree with the full reviews' on those repos, with each disagreement explained.

## 12. Other people in the review

The review counts other people only as a reason for care: stars, forks and issues from others make it prefer archive to make-private, a licence fix names anyone else with commits, and the fix prompt opens a pull request when others commit. It never shows who else built the repo, or whether the people who came to it got an answer, though both say as much about the repo as its stars do. A collaborator reading the page notices an issue from a stranger left unanswered for two years, or a README in the first person singular over someone else's commits.

Add to the Outcomes panel, as context with no pass or fail:
- **Contributors**: everyone else with commits, from `git shortlog -sne` on the clone (which works on claude.ai), by login where GitHub links one and by name otherwise, never by email address, with their number of commits and their last.
- **Waiting on you**: open issues and pull requests opened by other people, each with its age and whether the owner has replied.

And use them:
- **Tone** flags a README that presents shared work as the user's alone, such as a first-person history over commits that are mostly someone else's. The fix credits them by name.
- **Before archiving** and **keep** gain a draft reply for each open issue or pull request from someone else, in the fix prompt, for the user to post. The review never posts it.

The smaller item on contributions is part of this one, since it reads the same outside pull requests:
- **Says whether it takes contributions**: Way in checks that a visitor can run or reuse a repo, but not that the repo says whether it wants contributions, or that its settings agree with what it says: a README that asks for issues when issues are turned off, "pull requests welcome" on an archived repo, or no word either way on a repo with outside pull requests waiting. Add it to Way in, as a flag rather than a fail. A repo that doesn't want contributions passes once it says so. Item 5's Practice panel would check the CONTRIBUTING file and issue templates that a repo inviting contributions needs. Done when a review flags each of the three cases above, and passes a repo that says it doesn't take contributions.

Its rules match the `stargazers` skill's: public data only, no email addresses, never contact anyone.

**Done when** a review of a repo with commits from someone else and an unanswered issue from a stranger lists both in Outcomes, flags Tone if the README doesn't credit the other contributor, and puts a draft reply in the fix prompt.

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

## 13. Contributions to other people's projects

A merged pull request to someone else's project is some of the best evidence of how the user works with others: someone else's maintainers reviewed it and took it. Nothing shows it today. Triage reads the user's pull requests to a fork's parent, but only to decide about the fork, and an upstream contribution made without a fork on the account is never seen.

A new skill, `contributions`, would list the user's merged pull requests to repos they don't own, from issue search (`search/issues?q=author:LOGIN+type:pr+is:merged+-user:LOGIN`, which answers on claude.ai too), and sort them into three groups:
- **the user's own organisations' repos**, which `-user:` doesn't leave out. They're the user's own work, so they're left out of this list and counted instead;
- **employers' repos**, work done for a job. The user says which owners were employers, kept outside the plugin, as in Author identities below: the same employer often shows up both as an organisation here and as an email domain on old commits. They're listed apart, since whether to show them is the user's call;
- **other people's projects**, the open-source contributions: one entry per repo, with its stars, the number merged, the dates and a line on what each did, from its title, most-starred repo first.

Search gives at most 100 results a page and 1,000 in all, so paginate and say when the total runs past that. Like `stargazers`, it uses public data only and contacts no one. Profile review (item 6) would use the third group to say which contributions to mention in the profile README, and triage would use it to tell a fork whose work went upstream from one whose work didn't.

A search by hand on 2026-11-19 shows the shape on this account: 288 merged pull requests to repos not under `tcrossland`, 152 of them to the user's own `mailcellar` organisation, most of the remaining 136 to an employer's organisation, and the rest to open-source projects, among them `erlang/otp`, `elixir-lang/elixir`, `elixir-lsp/elixir-ls`, `beancount/fava` and `explosion/spacy-dev-resources`.

The smaller item on author identities is part of this one, since both need the same list of the user's past identities:
- **Author identities**: let the user list their past commit email domains, kept outside the plugin (in a gitignored file or an environment variable), so triage can tell their unlinked commits from other people's without asking. Done when triage reads the list and marks matching commits as the user's.

**Unverified**: how the skill finds the user's own organisations on claude.ai, where `user/orgs` is refused (`list_repos` lists repos of other owners the user can push to, which may be enough), and whether search reaches every old pull request.

**Done when** it lists the user's merged pull requests to other people's projects with the three groups apart, the counts add up to the search's total, and "Don't deselect date unless datepicker is multidate" to `uxsolutions/bootstrap-datepicker`, merged 2014-12-10, is among them.

## 6. Profile review

The profile page is the first thing a visitor sees. A profile README (the `OWNER/OWNER` repo), the bio, the pins and the featured repos aren't checked together today.

A new skill, `profile-review`, would:
- check the bio and the pins, reusing the pin ranking from overview mode;
- draft a short profile README in the house style that introduces the featured repos;
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

- **Three most-starred repos in `stargazers`**: it reads the first 100 repos only, and the API can't sort them by stars, so for someone with more than 100 repos the three can be wrong. Paginate, then sort by stars.
- **Fix prompts on the overview**: the overview page links each repo's scorecard but has no fix prompt, so acting on an overview means opening each scorecard in turn. Add a copy button to each row that has failing or flagged questions, copying that repo's fix prompt as its scorecard builds it (`fixPrompt` with every item). Keep one prompt per repo, not one for all of them: each runs in its own Claude Code session in that repo. Done when the overview's JSON carries each repo's `fixPrompt`, each row's button copies the same text as its scorecard's "All", and a template test checks it.
- **README links that don't ship**: the README is in the zip, but its "Working on it" section links to `docs/`, which isn't. Move that section to `docs/README.md`, or have `scripts/package.sh` leave it out.

## Done

### Reply counts from the JSON

Step 6's reply counted its pass, fail and flagged statuses by hand, and in a review on 2026-11-19 got 2 · 0 · 5 where the scorecard had 0 · 5 · 2. Since 0.2.6 a script in Step 6 prints the counts from the run's JSON, and refuses to count when there aren't seven questions or a status is unknown. Step 7 runs the same script on the overview's JSON for its per-repo entries. `tests/test_reply_counts.py` runs it on sample runs of both.

### 0. Prove the current version on claude.ai

0.2.4 was uploaded and every mode run once on 2026-11-19, recorded in the doc "github-curator 0.2.4: test report". Each run finished and published:
- the review of spacy-annotator recommended archive and keeping it pinned, with all seven questions passing, and one item before archiving still to do, where none was expected: third-party text in the repo with no source named. That's a finding about the repo, not a fault in the plugin;
- the overview of stat-arb-from-scratch and claude-code-methodology passed;
- triage listed 82 repos through the `list_repos` fallback, but marked none clear (item 11);
- stargazers listed 13 stargazers but read no profiles (item 11, which now covers what to show then).

The scorecard template loaded through its relative link, pins came through WebFetch, GraphQL is refused, and `argument-hint` caused no trouble. Each is now in `docs/github-facts.md`.
