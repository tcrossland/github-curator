# Design notes

Why the skills work the way they do. `SKILL.md` holds instructions only, because everything in it loads on every run; the reasons live here. Read this before changing a rule, so a change doesn't quietly undo one of these choices.

## The review only recommends

Neither skill archives, unarchives, deletes, pins, closes an issue or pull request, or changes a repo's visibility. Each of those changes what other people see or loses something (stars, watchers, read-only history), so each is the user's call. Where a step is mechanical, the review hands the user the command: the triage page lists `gh repo delete OWNER/REPO` without `--yes`, so each one still asks for confirmation.

## The seven questions, and what isn't scored

The seven questions judge the page as a visitor meets it, in order of importance, with Hook first. They have three statuses and no numbers: a threshold would invite gaming the score instead of fixing the page.

Outcomes (stars, traffic, stargazers) and similar repos are context. They never change a status or the verdict: there's no bar a repo should reach, and a niche repo can be excellent with few stars.

A private repo is checked as it would read once public. Findable is flagged rather than failed when visibility is its only gap, because making it public is a decision, not a defect.

## The recommendation

There are five actions, one per repo: keep, publish, archive, make-private and delete. The tie-breaker is "prefer the action that loses least": archive over make-private when anyone else has starred, forked or opened an issue, and make-private over delete whenever anything of the user's is in the repo.

The checklist before archiving comes from the work done on a real project before it was archived. A finished project archived with a proper account of what it was, why it stopped and what the author would do differently is a stronger portfolio piece than an unexplained abandoned repo.

## A scanner for secrets before publishing

Reading `git log` for secrets is weak over a long history, so the check before publishing runs a scanner. Of the scanners compared on 2026-11-20, betterleaks and gitleaks both scan the full history locally under MIT; betterleaks is maintained by gitleaks's original author and was the user's pick. trufflehog is AGPL-3.0, and GitGuardian's ggshield sends the code to its service. Calling a tool installed on the user's machine isn't bundling it, but a copyleft tool still wasn't wanted.

- **Detection only.** Both major versions can send each secret found to its provider to test it. That would send the user's secrets to third parties from a review that only recommends, so the script never asks for it, and with v2 turns it off explicitly, since an environment variable can turn it on.
- **Both versions.** Homebrew installs v1 while v2 is a release candidate with other flags and another report format. The script picks by `betterleaks version` and one `jq` reads both reports, so a user on either gets the scan.
- **Redacted, and never copied.** The report holds no secret values, and the review never copies one into the scorecard, the fix prompt or the reply, which are published or pasted elsewhere.
- **Findings stay out of the fix prompt.** Removing a secret from the history means rewriting it, which a commit can't do, and the key has to be revoked at its provider first. Both are the user's.
- **No install.** The review doesn't install software. Without betterleaks it searches the history as before, marks the item `todo` and says the scan didn't run, so a missing scan never passes silently.

## Feature is separate from the action

Featuring (pinning on the profile) is a yes or no alongside the action, not a sixth action, because the two combine: an archived project can still be one of the best pieces on a profile. Pinning is a step towards featuring, not a decision of its own. A profile shows at most six pins, so featuring is a choice made across all of the user's repos, which is why overview mode ranks the pins.

## Triage settles only what loses nothing

Triage reads the API alone, so it can't judge a page. It calls a repo `clear` only when deleting it loses nothing of the user's and nothing anyone else uses: an empty repo, or an unchanged fork nobody else has starred, forked or opened an issue on, and that isn't pinned. Everything else gets a provisional action and goes to the full review.

A fork with commits beyond its parent is never clear. A real run showed why: a fork looked like it held nothing of the user's, because GitHub's author filter found none of their commits, yet it held six commits they had made under an email not linked to their account.

## Similar repos

They show what a repo adds, which topics it lacks, and where to point readers of an archived repo. They are described only from what their own pages say, never as copying or influencing one another, the same rule as the `stargazers` skill. GitHub search can't find tools hosted elsewhere, so projects the README names are added by hand.

## Most-starred repos in `stargazers`

A stargazer's three most-starred repos say most about their field, but GitHub can't list someone's repos sorted by stars (`docs/github-facts.md`), so the skill reads every page and sorts them itself. That costs one call per 100 repos: one for most people, but tens for an organisation with thousands. Repository search can sort by stars in one call, and works on claude.ai, but its limit is 30 requests a minute, which a run of 30 profiles, each with an organisation, would pass.

## Three groups in `contributions`

A merged pull request to someone else's project is evidence someone else's maintainers reviewed and accepted, but not every pull request to a repo the user doesn't own is that. Issue search's `-user:LOGIN` leaves out only the user's own account, so pull requests to the user's own organisations come back too; on the account it was built on they were more than half. Those are counted, not listed. The user's own organisations are the ones they're an admin of, since a membership alone could be an employer's.

An employer's repos can't be told apart from the API: on that account the employer's 72 pull requests went to public repos, so visibility doesn't separate them. So the user names their employers, with `employers:` or in their own instructions or memory, which keeps the names out of the plugin and works on claude.ai, where there's no local file to read. Without them, the reply names the owners with the most merged pull requests and asks. Pull requests to private repos are searched apart (`is:private`) and counted without their names, because a visitor can't see them.

The groups are counted by a script from the search's own results, and its total is checked against the search's `total_count`, for the same reason the review's reply counts come from the page's data: counts made by hand drift. Stars come from one repository search with up to 40 `repo:` qualifiers rather than one call per repo, because `repos/OWNER/REPO` is refused on claude.ai for any repo not attached to the session, while search answers there.

## Other people in the review

Who else built a repo, and whether the people who came to it got an answer, say as much about it as its stars, so the Outcomes panel lists them: Contributors and Waiting on you. Like the rest of the panel they get no pass or fail; they feed Tone, Way in and the fix prompt instead.

Contributors come from the commits API rather than `git shortlog` on the clone: a public repo is cloned with `--depth 1`, which holds one commit, and the API gives each commit's login where GitHub links one, so a person is named by login and otherwise by the name on their commits, never by email address. A commit with no login counts as the user's when its name appears on any commit carrying the user's login: on the account it was built on, one repo had 8 of its 17 commits under the user's name with no linked login, and a rule that counted only logins would have listed the user as a contributor to their own repo. A script groups them, as the reply counts are, so the numbers on the page aren't counted by hand.

Tone is flagged, not failed, for shared work presented as the user's alone, because how much credit a contribution needs is a judgement the user makes; the fix names the others so the change is easy. Whether a repo takes contributions is a flag on Way in for the same reason, and it's met by saying either way: a repo that doesn't want them is fine once it says so.

The fix prompt drafts a reply to each issue or pull request waiting on the user, under its own status (`reply`), so the page's filter can show the replies apart from the edits. The review never posts one, and the prompt tells Claude Code not to either: a reply speaks for the user, so it's theirs to post, edit or drop.

## Steps for one mode live in their own file

`SKILL.md` loads in full on every run, so a single review used to carry the overview and triage steps it never runs. Those steps are in `overview.md` and `triage.md` beside it, read only in their mode, so a single review loads the shared rules and Steps 1 to 6, and changes to triage (item 11 rewrites it) don't grow every review. An overview reads its file before starting, since it holds how an overview logs its time, not only Step 7. Each mode file names the sections of `SKILL.md` it relies on.

The quote checker is a file, `verify_run.py`, copied into the working folder the way the template is, so it's run as written rather than retyped from the page. The supporting files load on claude.ai by the same route as the template, which was seen to work there (`docs/github-facts.md`); a script copied that way has been seen to run in Claude Code, and a single review there left the mode files unopened, but it hasn't been tried on claude.ai yet.

## One list of Claude Code's tools

The steps name claude.ai's tools (`add_repo`, `list_repos`, `list_artifacts` and the rest), because claude.ai is where the GitHub access is narrowest and the steps were written around it. Claude Code has none of those names, and a run there had to guess. `SKILL.md` maps each one to what Claude Code uses in one list near the top, rather than at each step, so the steps read the same on both and the mapping can be checked in one place. Without an artifact tool the run falls back to `no-publish`, since a page saved as a file loses nothing and the reply can say so.

GraphQL is named once, in Step 1's pins, with where it works and where it's refused. Before, the settings bullet said it wasn't available at all, which was true only on claude.ai, and the next bullet used it.

## The scorecard page

The page is one template, `skills/repo-review/scorecard-template.html`, filled with the run's JSON. It renders all three modes: a single review, the overview and triage. It's a separate file so it isn't retyped on every run. A re-run republishes to the same artifact, so the page keeps one URL and can show what changed since the last check. Scorecards published before the skill was renamed have the title "Portfolio repo check: …", and re-runs still find them.

## Timing

Every page carries the time and the GitHub requests each step took, so a change made to speed a mode up can be measured. The times are wall-clock from the end of one step to the end of the next, so they include Claude's own work between tool calls. That's what the user waits for, but it can't be told apart from time spent waiting on GitHub, and a skill can't read its own token use.

The request count comes from the rate limit's `core.used`, read at each step's end, rather than from Claude counting its own calls: reading the rate limit costs no request, and it counts every page of a paginated call, which a count of commands would miss. Search requests have their own count in the rate limit, but it resets every minute, so it can't be read across a step; those are counted by hand. GraphQL has its own limit, so it isn't counted. Traffic requests don't raise `core.used` at all (`docs/github-facts.md`); a review always makes the same four, so the skill names the gap rather than adding a hand count for it. Every timing line runs in one shell, so the log has one file and one clock. A step that spans GitHub's hourly reset has no count. Reads of the rate limit can also disagree within one window (`docs/github-facts.md`): resets a second apart, and now and then a read from what looks like a fresh window. So the conversion takes resets up to a minute apart as one window: a real reset starts a new hour-long window after the old one ends, so it moves the reset on by an hour or more. It gives no count across a read whose `used` falls. A stray read then costs the two rows either side of it, as a failed read does, and a review's total, from its first and last lines, still holds. Anything else using the same GitHub account at the same time inflates the count: a claude.ai session and the user's own `gh` were seen sharing one count. The logging line keeps `gh`'s output only when the call succeeds, because on an HTTP error `gh` prints the error body to stdout, and the conversion skips any line it can't read.

Each step's line goes in a command of its own. A line is stamped when its command runs, and Claude writes a whole command before it runs, so anything written into the same command as the line is timed to the step the line closes. In the cold overview of 2026-11-20, one command wrote the `Compare` line and then the whole page's JSON, so `Compare` took 35 s and the two steps after it 1 s each. A separate command costs one more tool call per step, a few seconds in a run of several minutes, and keeps each step's time its own.

The quote checker reads the questions from the run's JSON, so Step 4 starts the JSON with them and Step 5 adds the rest. `Verify and recommend` includes writing the questions, and `Build` the rest. Before, Timing said `Build` wrote the JSON while Step 4 already needed it, so where the writing was timed depended on how a run read the two.

An overview reviews its repos one at a time. Each log line closes a step that began at the line before it, and the request count is the account's, so two reviews run side by side can't be told apart: in the first overview logged, two repos' steps were interleaved, and each review's rows took in the other's work, while the overview's own rows gave one repo 356 s and the other 1 s. Running them in turn costs little extra time, since a run's time goes mostly to Claude's own work rather than to waiting on GitHub, and it keeps each repo's rows and the overview's per-repo times true.

## Where the fix prompt's edits land

The fix prompt follows the repo's own rules on branches first, and the user's instructions over both. Without either, a public repo, or one others commit to, gets a branch and a pull request, because its main branch is what visitors and contributors see. A private repo only the user commits to gets commits on the current branch, left unpushed: a pull request there is a review step for an audience of one, and the unpushed commits give the user the same chance to review.

## One fix prompt per repo on the overview

The overview carries each repo's fix prompt as its scorecard has it, with a copy button on that repo's row, so acting on an overview doesn't mean opening every scorecard. Each prompt stays separate, and copies the same text as the scorecard's "All": a fix prompt's edits, branch and checks belong to one repo, and Claude Code runs it in a session in that repo, so one prompt for several repos would have nowhere to run. The page builds the text with the scorecard's own function, so the two can't drift apart.

## Arguments are keywords, not placeholders

Each skill reads its arguments as words (`overview`, `triage forks`, `org:NAME`, `since:2026-01-01`, `no-publish`) rather than through Claude Code's positional placeholders (`$0`, `$name`). The modes take lists of any length, and a draft can be pasted text with spaces, so a fixed position for each argument would misread most calls. The `argument-hint` in each skill's frontmatter shows the words in Claude Code's autocomplete.

An organisation's triage is stricter than the user's own. Other people may rely on an organisation's repos, and only its admins can archive or delete them, so an unchanged fork there goes to review instead of being a clear delete, and a repo the user isn't an admin of is marked as an admin's call. Its page has its own title, so it doesn't replace the triage of the user's own repos.

`no-publish` exists for working on the skill: a test run of a changed rule or template would otherwise republish the live scorecard.

## Reply counts come from the page's data

The reply's pass, fail and flagged counts are printed by a script from the page's JSON, not counted by Claude. Counted by hand they drifted: one review's reply said 2 pass, 0 fail, 5 flagged where its scorecard had 0, 5 and 2. The script reads the same data the scorecard renders, so the two can't disagree, and it refuses to count when there aren't seven questions or a status is unknown, since a wrong count is worse than none.

## Behaviour evals

The unit tests run the skills' code; they can't notice a rule change that flips a recommendation. The cases in `evals/` do: each gives one repo and the call the skill should make, for a rule that has gone wrong or nearly so in a real run, and each should fail when its rule is cut from the skill. `scripts/evals.sh` runs them with `claude plugin eval`, which also runs each case without the plugin, so the report shows how much of each call comes from the skill rather than from Claude's own sense.

The cases run offline. The eval refuses reads outside a run's workspace, the skill's own mode files included, so `scripts/evals.sh` grants Read on the plugin's `skills/` folder. A case's prompt holds everything `gh` and a clone would return, and tells Claude not to call them: the eval gives each run an empty workspace with no shell unless granted one, and a live repo would change under the case. The prompt asks for the calls as a JSON block, which `regex` graders check, rather than an `llm` judge reading the reply: the expected call is a fixed word, and a regex gives the same verdict every time. A grader checks for something present, never only for something absent: a run without the plugin writes no such JSON, so "no `todo` anywhere" passed it for free and made the plugin's gain look smaller than it was. A check that something is absent matches the JSON it would be absent from, with a lookahead.

Each case was tried with its rule cut out of the skill, and the run without the plugin is the same check taken to the limit. On 2026-11-20 every case failed all three runs without the plugin, though for the triage cases that's partly vocabulary: without the skill there's no `clear` or `review` to use. Cutting one rule's text made two cases fail: the unchanged fork's clause in triage's clear delete, and the whole licence rule for Way in (cutting only "names a licence that no file holds" wasn't enough, since the fixture has no licence file at all, which the rest of the rule covers). Three cases still passed, because the skill states their rule more than once: the private Findable rule in three places, and forks with commits are kept from clear both by the definition of clear and by counting commits with no login as possibly the user's. The archived repo's items stayed done with the "says plainly that it no longer runs" clause cut. A cut that leaves a case passing shows the call is held by more than one statement, so a change has to remove every one of them to flip it.

A run reads the skill as a user's would, so it costs a review's tokens; the suite isn't part of the unit tests. A change to a rule runs only the cases that guard it, once each and without the runs without the plugin, and the full suite runs before each release. A user only gets a change with a release, so that run catches a rule change that breaks another case before it ships, at the cost of finding out later than the commit. The repeat runs and the runs without the plugin answer questions about the version being shipped (does a call hold steady, how much of it comes from the skill), not about one commit. A rewrite of text every case reads runs every case once, since any call could shift. The Way in case runs three times and needs every run to pass, because in the 0.2.4 test runs one repo's Way in was flagged in one review and passed in the next on the same commit: a rule that leaves too much to judgement shows up as runs that disagree.

## What ships

Everyone a plugin is shared with receives every file in the upload. `scripts/package.sh` zips only the manifest, the skills, the README, the changelog and the licence (`LICENSE` and `NOTICE`), leaving out `docs/`, `tests/` and `scripts/`, which are for working on the plugin, not using it. The README ships, so it links only to files the zip holds, and the notes for working on the plugin are in `docs/README.md` instead; `tests/test_shipped_links.py` checks every relative link in a shipped file.

The changelog ships because the zip is all a user gets: the repo is private, and the commit history, written for working on the plugin, doesn't go in it. Each entry says what changed from the user's side, and is written in the same commit as the version it describes.
