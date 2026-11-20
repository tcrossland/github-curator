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

## Feature is separate from the action

Featuring (pinning on the profile) is a yes or no alongside the action, not a sixth action, because the two combine: an archived project can still be one of the best pieces on a profile. Pinning is a step towards featuring, not a decision of its own. A profile shows at most six pins, so featuring is a choice made across all of the user's repos, which is why overview mode ranks the pins.

## Triage settles only what loses nothing

Triage reads the API alone, so it can't judge a page. It calls a repo `clear` only when deleting it loses nothing of the user's and nothing anyone else uses: an empty repo, or an unchanged fork nobody else has starred, forked or opened an issue on, and that isn't pinned. Everything else gets a provisional action and goes to the full review.

A fork with commits beyond its parent is never clear. A real run showed why: a fork looked like it held nothing of the user's, because GitHub's author filter found none of their commits, yet it held six commits they had made under an email not linked to their account.

## Similar repos

They show what a repo adds, which topics it lacks, and where to point readers of an archived repo. They are described only from what their own pages say, never as copying or influencing one another, the same rule as the `stargazers` skill. GitHub search can't find tools hosted elsewhere, so projects the README names are added by hand.

## Most-starred repos in `stargazers`

A stargazer's three most-starred repos say most about their field, but GitHub can't list someone's repos sorted by stars (`docs/github-facts.md`), so the skill reads every page and sorts them itself. That costs one call per 100 repos: one for most people, but tens for an organisation with thousands. Repository search can sort by stars in one call, and works on claude.ai, but its limit is 30 requests a minute, which a run of 30 profiles, each with an organisation, would pass.

## Steps for one mode live in their own file

`SKILL.md` loads in full on every run, so a single review used to carry the overview and triage steps it never runs. Those steps are in `overview.md` and `triage.md` beside it, read only in their mode, so a single review loads the shared rules and Steps 1 to 6, and changes to triage (item 11 rewrites it) don't grow every review. An overview reads its file before starting, since it holds how an overview logs its time, not only Step 7. Each mode file names the sections of `SKILL.md` it relies on.

The quote checker is a file, `verify_run.py`, copied into the working folder the way the template is, so it's run as written rather than retyped from the page. The supporting files load on claude.ai by the same route as the template, which was seen to work there (`docs/github-facts.md`); a script copied that way hasn't been tried there yet.

## The scorecard page

The page is one template, `skills/repo-review/scorecard-template.html`, filled with the run's JSON. It renders all three modes: a single review, the overview and triage. It's a separate file so it isn't retyped on every run. A re-run republishes to the same artifact, so the page keeps one URL and can show what changed since the last check. Scorecards published before the skill was renamed have the title "Portfolio repo check: …", and re-runs still find them.

## Timing

Every page carries the time and the GitHub requests each step took, so a change made to speed a mode up can be measured. The times are wall-clock from the end of one step to the end of the next, so they include Claude's own work between tool calls. That's what the user waits for, but it can't be told apart from time spent waiting on GitHub, and a skill can't read its own token use.

The request count comes from the rate limit's `core.used`, read at each step's end, rather than from Claude counting its own calls: reading the rate limit costs no request, and it counts every page of a paginated call, which a count of commands would miss. Search requests have their own count in the rate limit, but it resets every minute, so it can't be read across a step; those are counted by hand. GraphQL has its own limit, so it isn't counted. Traffic requests don't raise `core.used` at all (`docs/github-facts.md`); a review always makes the same four, so the skill names the gap rather than adding a hand count for it. Every timing line runs in one shell, so the log has one file and one clock. A step that spans GitHub's hourly reset has no count. Reads of the rate limit can also disagree within one window (`docs/github-facts.md`): resets a second apart, and now and then a read from what looks like a fresh window. So the conversion takes resets up to a minute apart as one window: a real reset starts a new hour-long window after the old one ends, so it moves the reset on by an hour or more. It gives no count across a read whose `used` falls. A stray read then costs the two rows either side of it, as a failed read does, and a review's total, from its first and last lines, still holds. Anything else using the same GitHub account at the same time inflates the count: a claude.ai session and the user's own `gh` were seen sharing one count. The logging line keeps `gh`'s output only when the call succeeds, because on an HTTP error `gh` prints the error body to stdout, and the conversion skips any line it can't read.

Each step's line goes in a command of its own. A line is stamped when its command runs, and Claude writes a whole command before it runs, so anything written into the same command as the line is timed to the step the line closes. In the cold overview of 2026-11-20, one command wrote the `Compare` line and then the whole page's JSON, so `Compare` took 35 s and the two steps after it 1 s each. A separate command costs one more tool call per step, a few seconds in a run of several minutes, and keeps each step's time its own.

An overview reviews its repos one at a time. Each log line closes a step that began at the line before it, and the request count is the account's, so two reviews run side by side can't be told apart: in the first overview logged, two repos' steps were interleaved, and each review's rows took in the other's work, while the overview's own rows gave one repo 356 s and the other 1 s. Running them in turn costs little extra time, since a run's time goes mostly to Claude's own work rather than to waiting on GitHub, and it keeps each repo's rows and the overview's per-repo times true.

## Where the fix prompt's edits land

The fix prompt follows the repo's own rules on branches first, and the user's instructions over both. Without either, a public repo, or one others commit to, gets a branch and a pull request, because its main branch is what visitors and contributors see. A private repo only the user commits to gets commits on the current branch, left unpushed: a pull request there is a review step for an audience of one, and the unpushed commits give the user the same chance to review.

## Arguments are keywords, not placeholders

Each skill reads its arguments as words (`overview`, `triage forks`, `org:NAME`, `since:2026-01-01`, `no-publish`) rather than through Claude Code's positional placeholders (`$0`, `$name`). The modes take lists of any length, and a draft can be pasted text with spaces, so a fixed position for each argument would misread most calls. The `argument-hint` in each skill's frontmatter shows the words in Claude Code's autocomplete.

An organisation's triage is stricter than the user's own. Other people may rely on an organisation's repos, and only its admins can archive or delete them, so an unchanged fork there goes to review instead of being a clear delete, and a repo the user isn't an admin of is marked as an admin's call. Its page has its own title, so it doesn't replace the triage of the user's own repos.

`no-publish` exists for working on the skill: a test run of a changed rule or template would otherwise republish the live scorecard.

## What ships

Everyone a plugin is shared with receives every file in the upload. `scripts/package.sh` zips only the manifest, the skills, the README, the changelog and the licence (`LICENSE` and `NOTICE`), leaving out `docs/`, `tests/` and `scripts/`, which are for working on the plugin, not using it. The README ships, so it links only to files the zip holds, and the notes for working on the plugin are in `docs/README.md` instead; `tests/test_shipped_links.py` checks every relative link in a shipped file.

The changelog ships because the zip is all a user gets: the repo is private, and the commit history, written for working on the plugin, doesn't go in it. Each entry says what changed from the user's side, and is written in the same commit as the version it describes.
