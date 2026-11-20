# Step 8: triage

`repo-review` in triage mode, read only in that mode. The steps and sections it names (Step 1, Step 5, Timing, The recommendation) are in [SKILL.md](SKILL.md).

**Timing**: log as set out under Timing in `SKILL.md`, with the steps `List repos`, `Forks`, `Own repos`, `Sort` and `Build`.

Triage is a first pass over many repos, from GitHub's API alone. It settles the cases the API makes plain, gives every other repo a provisional action, and names the ones worth a full review. It never clones, runs the seven questions, lists stargazers or searches for similar repos, and, like the rest of this skill, it only recommends.

## Which repos

List the repos the user owns with `gh api --paginate 'user/repos?affiliation=owner&per_page=100'`. If that fails or plainly misses repos, use `list_repos`, and say in the footer which source was used. Then apply the filters given: `public` or `private` (visibility), `own` or `forks`, and `archived` (archived repos are left out unless it's given). With no filters, take every repo that isn't archived. Read the pinned repos as in Step 1.

With `org:NAME`, list that organisation's repos instead, with `gh api --paginate 'orgs/NAME/repos?per_page=100'`, and apply the other filters to them; take one organisation per run. Other people in an organisation may rely on its repos, and only its admins can archive, delete or change the visibility of one:
- The listing's `permissions.admin` says whether the user is an admin of each repo. When it's false, add the signal "needs an org admin": every action on that repo is an admin's call, not the user's.
- A repo is `clear` only when it's empty and the user is its admin. A fork with no commits beyond its parent goes to review, with the question of whether anyone in the organisation uses it.
- The signals for "each repo of the user's own" apply to every repo that isn't a fork.
- Title the page "Repo triage: NAME", so it stays apart from the triage of the user's own repos.

## Signals

From the listing, for each repo: `private`, `fork`, `archived`, `pushed_at`, `stargazers_count`, `forks_count`, `open_issues_count`, `description`, `topics`, `size`, `default_branch` and `license`. Then:
- **Each fork**: read its parent from `gh api repos/OWNER/REPO` (`.parent`), and count the commits the fork has that its parent doesn't, as in Step 1. Note when the parent is archived, and when there is no parent (it was deleted or the fork was detached: treat the repo as the user's own). When the fork has commits beyond its parent, read who made them from the same compare call (`.commits[] | .author.login, (.commit.author.email | split("@")[1]), .commit.message`; it lists at most 250). Count a commit as possibly the user's when its login is the user's, or when it has no login at all: commits made under an email that isn't linked to the user's account have none, so GitHub's `author=` filter misses them. Record the email domains of those, not the addresses, so the user can recognise a former employer's. When `ahead_by` runs into the thousands, or none of the listed commits look like the user's, the fork's default branch has most likely drifted from the parent's (an old `master` against a newer `main`): say so, and count the user's commits with `gh api --paginate 'repos/OWNER/REPO/commits?author=OWNER&per_page=100' --jq '.[].sha' | wc -l`. Then list the user's pull requests to the parent and whether each was merged: `gh api 'search/issues?q=repo:PARENT-OWNER/PARENT-REPO+author:OWNER+type:pr'` (`.items[] | .title, .state, .pull_request.merged_at`).
- **Each repo of the user's own**: the first lines of its README, from `gh api repos/OWNER/REPO/readme --jq .content | base64 -d | head -20`, and whether it says the project is unmaintained or archived. A 404 means there is no README. When `license` is null, add the signal "no licence"; when its `spdx_id` is `NOASSERTION`, add "licence not recognised by GitHub". A fork's licence is its parent's, so leave it out for forks.

Write each repo's signals as short facts, as in The recommendation.

## Sorting

Give each repo a provisional action from The recommendation, and mark it `clear` or `review`:
- **clear delete**: an empty repo (`size` 0); or a fork with no commits beyond its parent, that nobody else has starred, forked or opened an issue on, and that isn't pinned. Nothing of the user's is lost.
- **likely delete, to review**: a fork whose commits beyond its parent look like the ones the user's merged pull requests already brought upstream. The work survives in the parent, but the full review should confirm nothing else is in the fork.
- **review**: everything else, with the likeliest action and the question the full review has to answer ("does the README say what the changes were for?", "worth publishing?"). When the repo has no licence and the likeliest action is keep, publish or archive, say in the question that one is needed: the full review fails Way in without it, and every checklist before archiving, publishing or featuring asks for one. Triage never settles keep, publish, archive, make-private or feature: each depends on the page and the work, which only the full review reads.

Among the repos to review, put first the ones where the most is at stake: those pinned on the user's profile, private repos that may be worth publishing, and public repos others have starred, forked or opened issues on.

## The triage page

Write the run as JSON and publish it from the same template as Step 5 (or save it, with `no-publish`), titled "Repo triage" (or "Repo triage: NAME" for an organisation), with the icon `checklist`. Republish to an existing artifact of the same title if `list_artifacts` finds one, and compare with it: name the repos that have gone since (the user acted on them) and any whose provisional action changed. Its JSON:
- `triage`: `true`
- `title`: "Repo triage"; `subject`: how many repos, which filters and the listing's source; `date`
- `changes` (only when there was a previous triage): `since` (its date) and `items`
- `repos`: one object per repo with `name` (owner/name), `link`, `visibility` (`public` or `private`), `kind` (`own` or `fork`), `pinned` (`true` or `false`), `pushed` (date only), `stars`, `signals` (the short facts), `action` (the provisional action), `sure` (`clear` or `review`), `reason` (one sentence) and, for `review`, `question` (what the full review has to answer). List the repos to review in the order above, then the clear ones.
- `commands`: for the clear deletes, one `gh repo delete OWNER/REPO` per repo, without `--yes`, so that each asks the user to confirm; leave it out when there are none. Introduce them in `commandsNote`: deleting needs the `delete_repo` scope (`gh auth refresh -s delete_repo`), a deleted repo can be restored within 90 days unless it's part of a fork network with other repos in it, and the user runs them only if they agree.
- `next`: the command that reviews the first ten repos marked `review`, `/github-curator:repo-review overview` followed by their URLs in the order above, and `nextNote` saying how many are left for later runs
- `timings`: the rows from the triage log, as set out under Timing, with `searches` on `Forks` when it searched for pull requests
- `footer`: which repos were included and how they were chosen, the pins' source, and that triage reads only the API, so every `review` action is provisional

Never run the commands, and never archive, delete or change the visibility of anything during triage.

Reply in two lines: the counts (`N clear deletes · N to review`, with the provisional actions among those to review, such as `4 likely archive`), then the first three repos to review, with the question for each.
