# Step 7: overview

The last step of `repo-review` in overview mode, read only in that mode. The steps and sections it names (Steps 1 to 6, Timing, The recommendation) are in [SKILL.md](SKILL.md).

**Timing**: log as set out under Timing in `SKILL.md`. Review the repos one at a time. Finish each repo's review, through publishing (or saving) its scorecard, before making any call for the next, and don't run two repos' steps side by side or in one command. Each repo's review keeps its own log and shows it on its scorecard, and the next repo's log starts after the last one's `Build` line. The overview's log has one line per repo, named `OWNER/NAME`, written as its scorecard is published (or saved, with `no-publish`), then `Build`.

An overview runs the full review on every repo, so with more than a handful, run `triage` first and pass the repos it names to `overview`.

For `overview`, use the repo URLs given. If none are given, list the user's repos with `list_repos`, keep the ones the user owns, public and private, forks included, leaving out those already archived, and say in the overview's footer which repos were included and how they were chosen.

After each repo's scorecard is published (or saved, with `no-publish`), publish or save one more page from the same template, titled "Portfolio overview", with the icon `checklist`. Republish to an existing "Portfolio overview" artifact if `list_artifacts` finds one. Its JSON:
- `overview`: `true`
- `title`: "Portfolio overview"; `subject`: how many repos and which commits; `date`
- `verdict`: `fix` (the repo that needs attention first, and its most important fix) and `why` (one or two sentences). Pick the repo whose earliest failing question comes first; break ties by the most fails.
- `pins`: `current` (the pinned repos and gists now, as `owner/name` strings), `recommended` (up to six, in the order to pin them, chosen across every repo reviewed and the current pins that weren't), `source` (where the current pins came from) and `why` (one or two sentences on what changes and why). Rank the repos whose feature call is yes, and keep a current pin that wasn't reviewed unless something reviewed is clearly stronger.
- `repos`: one object per repo with `name` (owner/name), `link`, `action` (its recommended action), `feature` (`true` or `false`), `todo` (the number of `todo` items before the action and featuring, or 0), `statuses` (the seven statuses in order), `fix` (that repo's verdict fix), `stars`, `views` (14-day views, or "Not available"), `scorecard` (the scorecard's claude.ai URL, or its file path with `no-publish`), and `fixPrompt`: the repo's own scorecard `fixPrompt`, copied as it is with every item, left out when its scorecard has none. Keep one per repo; don't merge them into one prompt.
- `timings`: the rows from the overview's log, one per repo, then `Build`, as set out under Timing
- `footer`: which repos were included and how they were chosen

Reply in three lines: the repo that needs attention first with its fix; the recommended pins, in order; then one `name: ACTION (featured), N pass · N fail · N flagged` entry per repo, with "(featured)" only when its feature call is yes, separated by semicolons. Take that third line exactly as the counts script in Step 6 prints it from the overview's JSON (`python3 counts.py OVERVIEW.json`), not counted by hand; if it prints `cannot count`, fix that repo's `statuses` and rebuild the page first.
