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

- **Author identities**: let the user list their past commit email domains, kept outside the plugin (in their instructions or memory, as `contributions` takes their employers), so triage can tell their unlinked commits from other people's without asking. Triage's fork step now reads each commit's author name and email domain from git, so the list would let it mark those commits as the user's. Done when triage reads the list and marks matching commits as the user's.
- **WebFetch of GitHub pages on claude.ai**: WebFetch of a `github.com` page is refused with `URL_NOT_ON_ALLOWLIST` unless a web search in the chat found the URL first (seen 2026-11-21). Two steps rely on it there:
  - **Pins**: `repo-review` Step 1, and triage through it, read the pins from the profile page when GraphQL is refused, as it is in a claude.ai session's own shell. A web search for the user's own `github.com/OWNER`, used only to fetch that page, may be enough, but in a quick review on 2026-11-22 the chat searched for "github.com tcrossland" after the refusal and said the results held only other users' profiles (the chat's account, **unverified**), so the pins weren't read. Later that day, in a review on 0.6.0-dev.3, a chat said it read the pins from the profile page after GraphQL was refused, labelled "profile page summary, may not be complete", and reported no refusal (the chat's account, **unverified**: how it reached the page wasn't shown). Whether a search can be made to find the user's own profile is the first thing to settle.
  - **Stargazers' profiles**: `users/LOGIN` is refused too, so `stargazers` reads no profile and its lists say "Not available" with the reason. The skill forbids searching the web for a stargazer, so the choice is whether a search for the exact profile URL, used only to fetch that page, fits the rule, or whether the README says stargazers' profiles need Claude Code. The same run fetched 12 profiles at once, where the skill says one at a time.

  Done when a claude.ai triage reads the pins, and a claude.ai `stargazers` run reads profiles or the README says they need Claude Code.
- **Carry over a triage's reasons**: the second triage on claude.ai reused the previous page's reasons and questions word for word where a repo's signals hadn't changed, which the skill neither asks for nor forbids. Decide whether triage should: carrying them over keeps the page stable between runs and saves time, but hides a call that a rule change since would make differently. Done when `triage.md` says which, and `docs/design.md` says why.
- **Reviews side by side**: `docs/design.md` has an overview review its repos one at a time, since the request count is the account's and side-by-side reviews can't be told apart. Several repo URLs with no mode word now ask which mode to run, so they no longer start separate reviews at once, but an overview whose reviews run in subagents still can. On 2026-11-21 one review ran alone, then seven ran in subagents four at a time: by their timing logs they took 2,312 s between them and the last finished 817 s after the first began. Three things came up that the skill doesn't cover. Each review's `calls` included the others' requests, and the page has no field to say so, so each footer said it in a sentence the subagents were given. The reviews share the search limit of 30 a minute (`gh api rate_limit`); none was refused, and the retry after a minute that the subagents were told to use isn't in the skill. And nothing says how many may run at once. Done when the skill either rules side-by-side reviews out, or says how to run them (how many at once, what to do when a search is refused) and the page shows when a review's counts include other runs'.
- **Work logged in the wrong step**: in three of the eight reviews of 2026-11-21, run as subagents, work landed before the line of the step it belongs to, although each step's line had a command of its own. One started the run's JSON and ran `verify_run.py` before the `Questions` line; two looked for the previous scorecard after the `Get the draft` line; one wrote Step 5's JSON before the `Verify and recommend` line, leaving 4 s for `Build`. It recurred on 2026-11-21 in two reviews on 0.4.0: one logged `Questions` before writing the questions, and a subagent appended its `Compare` line in the same command that wrote the comparison list, which Timing forbids. Done when Timing says which step each of these belongs to, and a review run after the change shows none of them.
- **The user's own star in triage**: triage reads `stargazers_count` as interest from others, but the count includes the user's own star. On 2026-11-21 triage gave one repo "A finished prototype with a star" as its reason to archive, and that star was the user's own, given the day the repo was created. Triage never lists stargazers today (`triage.md`), so telling them apart changes that rule: one stargazers call for each repo with only a few stars would do it, and `stargazers` already leaves the user's own star out. Done when triage leaves the user's own star out of its signals and reasons, `docs/design.md` says why, and the timings show what it costs.
- **Eval cases that fail with their rule cut**: `quick-way-in-no-usage` and `similar-relations` guard the rules that went wrong in quick mode's first live check. On 2026-11-22, one run each with the rule cut from a copy of the plugin: both Difference graders failed, as they should, but the Way in grader and both Mention graders still passed. So those two calls are held by other statements (Step 2's question for Way in; the Archive bullet and the old wording for Mention), or the fixtures are easier than the live case, where the review ran in full and recommended keep. Done when each grader fails with its rule cut, from a fixture closer to the live case (for Mention, a keep review that runs the recommendation), or `docs/design.md` says why a passing cut is acceptable.
- **Tone's shared-work flag varies between runs**: the `other-people` eval case missed Tone's flag in one of three runs on Opus 5.5 (2026-11-21) and in one of three on Sonnet 5.5 (2026-11-22), the only miss in either suite. A rule that leaves too much to judgement shows up as runs that disagree (`docs/design.md`, Behaviour evals). Done when Tone's rule says plainly when shared work presented as the user's alone is flagged, and the case passes three runs out of three on both models.
- **Similar repos calls `repos/OWNER/REPO`**: on 2026-11-22 two claude.ai reviews, on 0.6.0-dev.2 and dev.3, called `repos/OWNER/REPO` for a similar repo, which Similar repos doesn't ask for, and each was refused with HTTP 403 (`GitHub access to this repository is not enabled for this session`); both went on from the search results. Done when Similar repos says the search results hold every field it needs and to call nothing under `repos/` for a similar repo, and a claude.ai review after the change makes no such call.
- **Which model for a full review**: with `--model sonnet` the eval suite passed as it does on Opus 5.5 at about half the cost a run, but the cases check fixed calls on small fixtures, not the judgement calls a real README needs (Hook, Defensible, Context). Done when full reviews of the same three real repos on Sonnet 5.5 and Opus 5.5 are compared question by question, `docs/design.md` records the result, and the README says which model to pick. Until then, the README's Try it section says which model the skills were tested on (the eval suite has run on Opus 5.5 and Sonnet 5.5, and one claude.ai check on Sonnet 5.5), so a user on another model knows what they're departing from.
- **Co-authors from commit trailers**: the review counts other people's commits from `repos/OWNER/REPO/contributors`, which counts commit authors only. For this repo it gave one contributor while GitHub's Contributors sidebar showed two, the second being Claude, named only in `Co-Authored-By` trailers, so the sidebar seems to count trailers (inferred from the counts, **unverified**). A repo whose human co-authors appear only in trailers would then look like solo work to Tone. Done when the inference is checked, and the review reads co-authors from the trailers (leaving out Claude and other tools) or `docs/design.md` says why not.
- **Progress during long runs**: a full review takes two to five minutes and an overview of ten repos about half an hour, with only tool calls to watch. Each step already logs a timing line; the run could also print one short line as each step or repo starts ("Step 2 of 6: the questions", "Repo 3 of 10: OWNER/REPO"). Done when every mode prints one, and only one, line per step or repo, and the timings show it costs nothing measurable.
- **The cost of a big run, before it starts**: before an overview or triage of more than about ten repos, say what it will take ("12 repos, about 35 minutes; on claude.ai, 12 approvals to attach them"), from the per-repo times in `docs/design.md`, and offer `quick` instead. Done when `overview.md` and `triage.md` say when and how to estimate, and a run past the threshold gives the estimate before its first step.
- **`repo-review` with no arguments**: `SKILL.md` names no case for a bare `/github-curator:repo-review`. It could offer the three ways in: review the repo in the current folder, a quick review of every repo, or a triage. Done when `SKILL.md` names the case and a bare run offers them.
- **What changed, in the reply**: Step 3 lists what changed since the last run, but Step 6's reply leaves it out, though a user re-running after fixing things wants it first. A line such as "Since 2026-11-21: Hook fail → pass; 2 fixes landed" would come from the comparison, counted by a script as the counts are. Done when a re-run's reply has the line, a first run's doesn't, and a test covers both.
- **Links between the pages**: each scorecard, the quick review, the triage page, the overview and Traffic history are separate artifacts found by title, and only the overview links to scorecards. Quick and triage rows could link to a repo's scorecard when one exists, and a scorecard's header to the latest quick review, triage and overview, from one listing of the user's artifacts. Done when each page links to the others it names, and a template test covers each link.
- **Review one repo from a quick or triage row**: those pages give one `next` command for ten repos. A copy button on each row, giving `/github-curator:repo-review URL`, as the overview's rows copy their fix prompts, would let the user pick. Done when each row with a fail, flag or `review` has the button, and a template test covers it.
- **Fewer approvals on claude.ai**: in Manual mode each `add_repo` call needs an approval, so attaching N repos takes N (`docs/github-facts.md`). Auto mode attached without a prompt in the 0.6.0-dev.3 check, but its check refused `add_repo` in some earlier chats, which is why attaching goes through Manual mode (`docs/design.md`). Trying Auto first and asking for Manual only after a refusal would save most approvals. Done when a claude.ai check shows how often Auto refuses, and the Attaching rule follows from it.
