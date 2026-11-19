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

## The scorecard page

The page is one template, `skills/repo-review/scorecard-template.html`, filled with the run's JSON. It renders all three modes: a single review, the overview and triage. It's a separate file so it isn't retyped on every run. A re-run republishes to the same artifact, so the page keeps one URL and can show what changed since the last check. Scorecards published before the skill was renamed have the title "Portfolio repo check: …", and re-runs still find them.

## What ships

Everyone a plugin is shared with receives every file in the upload. `scripts/package.sh` zips only the manifest, the skills, the README and the licence (`LICENSE` and `NOTICE`), leaving out `docs/`, `tests/` and `scripts/`, which are for working on the plugin, not using it.
