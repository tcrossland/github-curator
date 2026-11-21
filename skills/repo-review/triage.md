# Step 8: triage

`repo-review` in triage mode, read only in that mode. The steps and sections it names (Step 1, Similar repos, Step 5, Timing, The recommendation) are in [SKILL.md](SKILL.md).

**Timing**: log as set out under Timing in `SKILL.md`, with the steps `List repos`, `Attach` (only when it ran), `Forks`, `Own repos`, `Sort` and `Build`.

Triage is a first pass over many repos, from GitHub's API and git alone. It settles the cases they make plain, gives every other repo a provisional action, and names the ones worth a full review. It never makes a full clone, runs the seven questions, lists stargazers or searches for similar repos, and, like the rest of this skill, it only recommends.

## Which repos

List the repos the user owns with `list_repos`, keeping those whose owner is the user, and say in the footer which source was used (in Claude Code, `user/repos`, as the list at the top of `SKILL.md` says). Then apply the filters given: `public` or `private` (visibility), `own` or `forks`, and `archived` (archived repos are left out unless it's given). With no filters, take every repo that isn't archived. Read the pinned repos as in Step 1.

The signals below need each repo's listing fields. `user/repos` gives them; `list_repos` doesn't, so on claude.ai read them for the public repos from one search, `gh api --paginate 'search/repositories?q=user:OWNER+fork:true&per_page=100'` (`fork:true` keeps the forks in), and for each private repo from `gh api repos/OWNER/REPO` once it's attached.

**The previous triage.** Look for the previous page now, as set out under The triage page, and read its `repos`. A fork's parent doesn't change, so each fork's `parent` there is used again rather than read anew.

**Attaching, on claude.ai.** There a repo's API answers, and a private repo clones, only once the repo is attached with `add_repo`; git clones a public repo without it. So attach only what triage can't do without: the private repos in the filters, and the forks whose parent the previous page doesn't give. When there are any:
1. In one message, say how many of each and name them, and ask the user to switch this chat to Manual mode, so each `add_repo` waits for their approval rather than for Auto mode's check, which refuses it unpredictably, and to reply once they agree to the repos being attached. A first triage has no previous page, so it attaches every fork and private repo: say so, and that a triage run from Claude Code attaches nothing. Wait for the answer.
2. Attach each with `add_repo` and `access: "push"`, one at a time. Don't clone them, whatever its result says: the steps below clone only what they need.
3. A repo that isn't attached (refused, or the user declined) can't be settled: it goes to review, with the signal "not attached: REASON".

Say in the footer how many repos were attached, and when this was a first triage on claude.ai, that it attached every fork and private repo.

With `org:NAME`, list that organisation's repos instead, with `gh api --paginate 'orgs/NAME/repos?per_page=100'`, and apply the other filters to them; take one organisation per run. On claude.ai that path is refused and nothing else gives the user's admin rights, so stop there and say in one line that an organisation's triage runs from Claude Code. Other people in an organisation may rely on its repos, and only its admins can archive, delete or change the visibility of one:
- The listing's `permissions.admin` says whether the user is an admin of each repo. When it's false, add the signal "needs an org admin": every action on that repo is an admin's call, not the user's.
- A repo is `clear` only when it's empty and the user is its admin. A fork with no commits beyond its parent goes to review, with the question of whether anyone in the organisation uses it.
- The signals for "each repo of the user's own" apply to every repo that isn't a fork.
- Title the page "Repo triage: NAME", so it stays apart from the triage of the user's own repos.

## Signals

From the listing, for each repo: `private`, `fork`, `archived`, `pushed_at`, `stargazers_count`, `forks_count`, `open_issues_count`, `description`, `topics`, `size`, `default_branch` and `license`. Then:
- **Each fork**: its parent comes from the previous page or, for a fork not on it, from `gh api repos/OWNER/REPO --jq '.parent.full_name'`. When there is no parent (it was deleted or the fork was detached), treat the repo as the user's own. Read whether each parent is archived from one repository search naming them all, `gh api 'search/repositories?q=repo:A+repo:B+fork:true&per_page=100'` with up to 40 `repo:` qualifiers per search; a parent missing from the results was deleted or is private.
  Count and list the commits the fork has that its parent doesn't with Step 1's git commands. A commit is the user's when its author name is their login or their name (`gh api user --jq '.login, .name'`), and possibly theirs when the name could be (a short form, initials). Git carries no logins, and commits made under an email not linked to the user's account were missed by GitHub's author filter, so judge by the name, and record the email domains of the user's commits so they can recognise a former employer's. When the count runs into the thousands, or none of the commits look like the user's, the fork's default branch has most likely drifted from the parent's (an old `master` against a newer `main`): say so, and count the user's commits in the fork's whole history with `git -C "forks/REPO.git" rev-list --count --author='LOGIN' --author='NAME' HEAD`.
- **The user's pull requests to the parents**: one search for them all, rather than one per fork, since the search API allows 30 requests a minute. Its pages come 100 pull requests at a time:
  ```sh
  gh api --paginate 'search/issues?q=author:OWNER+type:pr+-user:OWNER&per_page=100' --jq '.items[] | [(.repository_url | sub(".*/repos/"; "")), .state, ((.pull_request.merged_at // "")[:10]), .title] | @tsv' > prs.tsv
  ```
  Each line is a pull request: the repo it went to, its state, the date it was merged (empty when it wasn't) and its title. Take each fork's from the lines for its parent. Search returns at most 1000 results, so if `prs.tsv` has 1000 lines, say in the footer that a fork's pull requests may be missing. If `gh` stops with an error, a page was refused: say so in the footer, and use the lines it wrote. Count the searches for the `Forks` row.
- **Each repo of the user's own**: the first lines of its README, read as in Similar repos, and whether it says the project is unmaintained or archived. Skip it for an empty repo (`size` 0). When `license` is null, add the signal "no licence"; when its `spdx_id` is `NOASSERTION`, add "licence not recognised by GitHub". A fork's licence is its parent's, so leave it out for forks.

Write each repo's signals as short facts, as in The recommendation.

## Sorting

Give each repo a provisional action from The recommendation, and mark it `clear` or `review`:
- **clear delete**: an empty repo (`size` 0); or a fork with no commits beyond its parent, that nobody else has starred, forked or opened an issue on, and that isn't pinned. Nothing of the user's is lost.
- **likely delete, to review**: a fork whose commits beyond its parent look like the ones the user's merged pull requests already brought upstream. The work survives in the parent, but the full review should confirm nothing else is in the fork.
- **review**: everything else, with the likeliest action and the question the full review has to answer ("does the README say what the changes were for?", "worth publishing?"). A repo whose parent or commits couldn't be read, or that wasn't attached, is here too, with the question of what stopped it. When the repo has no licence and the likeliest action is keep, publish or archive, say in the question that one is needed: the full review fails Way in without it, and every checklist before archiving, publishing or featuring asks for one. Triage never settles keep, publish, archive, make-private or feature: each depends on the page and the work, which only the full review reads.

Among the repos to review, put first the ones where the most is at stake: those pinned on the user's profile, private repos that may be worth publishing, and public repos others have starred, forked or opened issues on.

## The triage page

Write the run as JSON and publish it from the same template as Step 5 (or save it, with `no-publish`), titled "Repo triage" (or "Repo triage: NAME" for an organisation), with the icon `checklist`. Republish to an existing artifact of the same title if `list_artifacts` finds one, and compare with it: name the repos that have gone since (the user acted on them) and any whose provisional action changed. Its JSON:
- `triage`: `true`
- `title`: "Repo triage"; `subject`: how many repos, which filters and the listing's source; `date`
- `changes` (only when there was a previous triage): `since` (its date) and `items`
- `repos`: one object per repo with `name` (owner/name), `link`, `visibility` (`public` or `private`), `kind` (`own` or `fork`), `pinned` (`true` or `false`), `pushed` (date only), `stars`, `signals` (the short facts), `action` (the provisional action), `sure` (`clear` or `review`), `reason` (one sentence), for `review`, `question` (what the full review has to answer), and for a fork, `parent` (the parent's owner/name, or `null` when it has none), so the next triage doesn't need to read it again. List the repos to review in the order above, then the clear ones.
- `commands`: for the clear deletes, one `gh repo delete OWNER/REPO` per repo, without `--yes`, so that each asks the user to confirm; leave it out when there are none. Introduce them in `commandsNote`: deleting needs the `delete_repo` scope (`gh auth refresh -s delete_repo`), a deleted repo can be restored within 90 days unless it's part of a fork network with other repos in it, and the user runs them only if they agree.
- `next`: the command that reviews the first ten repos marked `review`, `/github-curator:repo-review overview` followed by their URLs in the order above, and `nextNote` saying how many are left for later runs
- `timings`: the rows from the triage log, as set out under Timing, with `searches` on `List repos` and `Forks` when they searched
- `footer`: which repos were included and how they were chosen, the pins' source, what was attached, and that triage reads only the API and git, so every `review` action is provisional

Never run the commands, and never archive, delete or change the visibility of anything during triage.

Reply in two lines: the counts (`N clear deletes · N to review`, with the provisional actions among those to review, such as `4 likely archive`), then the first three repos to review, with the question for each.
