# Backlog

Ideas for the plugin, in the order to do them. Each says why it's worth doing and what done looks like. Anything not yet checked against its source is marked **unverified**.

## Summary

| # | Item | Kind | Size | Depends on | Status |
|---|---|---|---|---|---|
| 1 | [Traffic history](#1-traffic-history) | New skill and scheduled task | M | none | in progress |
| 6 | [Profile review](#6-profile-review) | New skill | M | none | todo |
| 10 | [Launch drafts](#10-launch-drafts) | New skill | M | 1 helps | todo |
| 5 | [Benchmark against good practice](#5-benchmark-against-good-practice) | Scorecard panel | L | none | todo |
| – | [Other smaller items](#smaller) | Fixes | S each | none | any time |

Sizes: S is an hour or two, M is a session, L is several sessions. Change Status to `in progress` when work starts. When an item is done, delete its section and its summary row, and take it out of other items' Depends on: the changelog and the commit that closes it record it. Keep a short section under Done only when an open item depends on what it found, such as figures, and keep only that part. A smaller item is simply deleted.

## 1. Traffic history

GitHub keeps traffic for 14 days only, so the scorecard's views, clones and referrers are lost after a fortnight. Nothing can show whether featuring or sharing a repo changed anything. This is the only item that loses something for every week it waits.

The `traffic` skill saves a snapshot of every public repo's stars, forks, daily views and clones and top referrers as one document in the database of a page titled "Traffic history", which charts them across snapshots, and `schedule` sets up a weekly task that runs it. The page exists, holding the hand snapshot of 2026-11-20 and one taken with the skill's script in Claude Code on 2026-11-21.

A claude.ai chat attached all 74 public repos in Auto mode and created the weekly task, which runs early on Mondays, and a run of it started by hand saved a snapshot of all 74 (`docs/github-facts.md`). The page holds four snapshots, three of them from 2026-11-21.

The review's Outcomes panel links to the page.

What's left is **the first run on schedule**: whether the weekly task saves a snapshot when nobody starts it. If it doesn't, the fallback is a scheduled task in the Claude Code desktop app.

**Done when** two weekly snapshots of every public repo are saved and charted on the page, the second by the weekly task on its schedule.

## 6. Profile review

The profile page is the first thing a visitor sees. A profile README (the `OWNER/OWNER` repo), the bio, the pins and the featured repos aren't checked together today. On claude.ai it reads the profile page through WebFetch, so it depends on the smaller item on WebFetch of GitHub pages there. `repo-review quick` leaves the profile README repo out for this skill, since Findable and Way in don't apply to it.

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

## Smaller

Each is done when the change is made and the tests pass, unless it says otherwise. They can be done at any time.

- **`contributions` on claude.ai**: its commands, run in a claude.ai chat on 2026-11-21, don't give Claude Code's groups (details in `docs/github-facts.md`). `gh api user` answers, but `user/memberships/orgs` is refused, and the fallback, the owners `list_repos` gives, missed an organisation and added a user account. The private search also found fewer pull requests than Claude Code does. The skill now says both in its reply on claude.ai. Done when a claude.ai run of the skill, on an upload that has it, shows both.
- **Secrets scan on claude.ai**: `repo-review` now fetches betterleaks 1.10.1 into the claude.ai VM, checked against the release's checksums, but no review on claude.ai has run it yet. Done when a review of a private repo on claude.ai, on an upload that has the fetch, runs the scan and its page says so. One claude.ai check, on an upload that has both this and the `contributions` change above, can close both.
- **Author identities**: let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. Triage's fork step now reads each commit's author name and email domain from git, so the list would let it mark those commits as the user's. Done when triage reads the list and marks matching commits as the user's.
- **WebFetch of GitHub pages on claude.ai**: WebFetch of a `github.com` page is refused with `URL_NOT_ON_ALLOWLIST` unless a web search in the chat found the URL first (seen 2026-11-21). Two steps rely on it there:
  - **Pins**: `repo-review` Step 1, and triage through it, read the pins from the profile page when GraphQL is refused, as it is in a claude.ai session's own shell. A web search for the user's own `github.com/OWNER`, used only to fetch that page, is enough.
  - **Stargazers' profiles**: `users/LOGIN` is refused too, so `stargazers` reads no profile and its lists say "Not available" with the reason. The skill forbids searching the web for a stargazer, so the choice is whether a search for the exact profile URL, used only to fetch that page, fits the rule, or whether the README says stargazers' profiles need Claude Code. The same run fetched 12 profiles at once, where the skill says one at a time.

  Done when a claude.ai triage reads the pins, and a claude.ai `stargazers` run reads profiles or the README says they need Claude Code.
- **Carry over a triage's reasons**: the second triage on claude.ai reused the previous page's reasons and questions word for word where a repo's signals hadn't changed, which the skill neither asks for nor forbids. Decide whether triage should: carrying them over keeps the page stable between runs and saves time, but hides a call that a rule change since would make differently. Done when `triage.md` says which, and `docs/design.md` says why.
- **A first triage on claude.ai**: none has run. Manual mode asks before every `add_repo`, and whether its approval prompt offers to allow `add_repo` for the rest of the chat is **unverified**. Done when the prompt's options are recorded in `docs/github-facts.md`.
- **The verdict for make-private and delete**: Step 4 makes the verdict's fix the first `todo` item or the action itself, but `verdict.question` still needs a number, which the template shows as "Most important fix · question N". On 2026-11-21 a make-private review gave 6 and a delete review gave 1, each by its own reasoning. The same make-private review read the action as "leave it private" for a repo that already was, and on 2026-11-22 a quick review, finding no action that fits a private repo not worth showing, gave keep with the question "does it stay private?". Done when Step 4 says what `question` holds for these actions (or the template shows none), and The recommendation says what make-private means for a private repo.
- **Several URLs without `overview`**: `/github-curator:repo-review URL URL ...` isn't a mode. On 2026-11-21 ten URLs ran as separate one-draft reviews in subagents (two of the repos no longer existed). Decide whether several URLs mean an overview, separate reviews, or a question to the user. Done when `SKILL.md` names the case and `docs/design.md` says why.
- **Reviews side by side**: `docs/design.md` has an overview review its repos one at a time, since the request count is the account's and side-by-side reviews can't be told apart. On 2026-11-21 one review ran alone, then seven ran in subagents four at a time: by their timing logs they took 2,312 s between them and the last finished 817 s after the first began. Three things came up that the skill doesn't cover. Each review's `calls` included the others' requests, and the page has no field to say so, so each footer said it in a sentence the subagents were given. The reviews share the search limit of 30 a minute (`gh api rate_limit`); none was refused, and the retry after a minute that the subagents were told to use isn't in the skill. And nothing says how many may run at once. Done when the skill either rules side-by-side reviews out, or says how to run them (how many at once, what to do when a search is refused) and the page shows when a review's counts include other runs'.
- **Work logged in the wrong step**: in three of the eight reviews of 2026-11-21, run as subagents, work landed before the line of the step it belongs to, although each step's line had a command of its own. One started the run's JSON and ran `verify_run.py` before the `Questions` line; two looked for the previous scorecard after the `Get the draft` line; one wrote Step 5's JSON before the `Verify and recommend` line, leaving 4 s for `Build`. It recurred on 2026-11-21 in two reviews on 0.4.0: one logged `Questions` before writing the questions, and a subagent appended its `Compare` line in the same command that wrote the comparison list, which Timing forbids. Done when Timing says which step each of these belongs to, and a review run after the change shows none of them.
- **The user's own star in triage**: triage reads `stargazers_count` as interest from others, but the count includes the user's own star. On 2026-11-21 triage gave one repo "A finished prototype with a star" as its reason to archive, and that star was the user's own, given the day the repo was created. Triage never lists stargazers today (`triage.md`), so telling them apart changes that rule: one stargazers call for each repo with only a few stars would do it, and `stargazers` already leaves the user's own star out. Done when triage leaves the user's own star out of its signals and reasons, `docs/design.md` says why, and the timings show what it costs.
- **Quick mode on claude.ai**: no quick review has run there. Repository search answers there with nothing attached, but whether `archived:false` gives the same results as in Claude Code is **unverified**, and a private repo's README needs it attached. The fixes from the first live check (description quotes checked against the saved listing, Way in failing a README with no usage, the profile README repo left out) haven't run live either. Done when a claude.ai quick run records in `docs/github-facts.md` what `archived:false` gave, and its page shows the description quotes checked.
- **Eval cases for quick mode and Similar repos**: every case skips similar repos and none runs `quick`, so no case guards their rules. Two went wrong in the first live check: a quick run flagged Way in for a README with a licence and no usage, and Similar repos' Differences remarked on other repos' READMEs. Done when a case guards each, and each fails with its rule cut.
- **Check the Claude Code tool list**: 0.2.14 added a list near the top of `repo-review`'s `SKILL.md` saying what Claude Code uses in place of each claude.ai tool, and what a run does with no artifact tool. In the desktop app, the triage of 2026-11-21 followed the list: it found the previous page with the Artifact tool and republished to it. Whether Claude Code outside the desktop app has an artifact tool is **unverified**. Done when a `claude -p` session's tool list is recorded in `docs/github-facts.md`, and the list's last line matches it.
