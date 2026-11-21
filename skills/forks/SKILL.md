---
name: "forks"
description: "List the forks of one of the user's GitHub repos that have commits of their own, what those commits change and who made them. Use when the user asks who forked a repo, what people did with their forks, or whether anyone builds on it."
argument-hint: "[OWNER/REPO …] [all]"
---

# Forks

A fork with commits of its own says more than a star: someone used the code and changed it. Find the forks of one of the user's public GitHub repos that hold commits the repo doesn't, say what those commits change and who made them, and pick out the ones worth a look. The repo review runs Steps 1 to 3 for its Outcomes panel, so a change to them changes the scorecard too.

The arguments are repo URLs or `OWNER/REPO` names, taken in turn, and one optional keyword:
- `all`: read every fork that was pushed to after it was made, not only the 30 most recently pushed. Each takes a fetch of a few seconds, so when that's more than 100 forks, say how many before starting.

With no repo given, run over every public repo the user owns that has forks, listed with `gh api --paginate 'user/repos?affiliation=owner&visibility=public&per_page=100' --jq '.[] | select(.forks_count > 0) | .full_name'`. On claude.ai that path is refused with HTTP 403; use `gh api --paginate 'search/repositories?q=user:LOGIN+fork:true&per_page=100' --jq '.items[] | select(.forks_count > 0) | .full_name'` instead, with the login from `gh api user`.

Work in the scratchpad, or a working folder of your own.

## Rules

- Use only what GitHub shows publicly: the forks listing through `gh api`, and the forks' commits through git. Don't search the web or other sites for a fork's owner, and don't record email addresses.
- Never star, follow, message, open an issue or pull request on, or comment on a fork or its owner: that's the user's call. If the user asks for one of these, do it only for the forks they name.
- Say what a fork's commits change. Never say its owner copied, took or was influenced by anything: forking is what the repo's licence and GitHub invite.

## Step 1: list the forks

On claude.ai, the API answers for a repo only once it's attached: attach each repo first with `add_repo` and `access: "push"` (a review has already attached its repo), asking the user once for permission for all of them. Don't clone them. The forks themselves need no attaching: git fetches a public fork without it. If a repo can't be attached, say so in one line and go on to the next.

First read the repo with `gh api repos/OWNER/REPO --jq '{full_name, private, forks_count, parent: .parent.full_name}'`, and use its `full_name` from here on. `parent` is set when the repo is itself a fork (Step 2 uses it). If the call returns 404, stop and say in one line that the repo doesn't exist or isn't visible to the user. If it's private, stop and say so in one line: a private repo's forks are private too, and visible only to the people it's shared with. If `forks_count` is 0, say there are no forks and stop.

Then list its forks, newest first, one line each:
```sh
gh api --paginate 'repos/OWNER/REPO/forks?sort=newest&per_page=100' --jq '.[] | [.full_name, .owner.type, .default_branch, .created_at[:10], .pushed_at[:10], .stargazers_count, .forks_count, (.pushed_at > .created_at)] | @tsv' > forks-REPO.tsv
```
Each line is a fork: its name, whether its owner is a `User` or an `Organization`, its default branch, the dates it was made and last pushed to, its stars and forks, and whether anyone pushed to it after it was made. The listing gives only the repo's direct forks; for each fork with forks of its own, list those the same way, appending to the file with `>>`, and so on until none is left. `forks_count` can be higher than the lines listed, since it counts forks GitHub no longer lists: say both numbers when they differ.

A fork that nobody pushed to after it was made holds nothing of its own (the last column is `false`): count those, but don't read them. Read the others in Step 2, the 30 most recently pushed unless `all` was given, and say how many are left out.

## Step 2: read each fork's commits

Clone the user's repo once, without its files, every branch and tag:
```sh
d="forks-of/REPO.git" && { [ -d "$d" ] && git -C "$d" fetch -q --prune origin '+refs/heads/*:refs/heads/*' '+refs/tags/*:refs/tags/*' || git clone -q --bare --filter=tree:0 "https://github.com/OWNER/REPO.git" "$d"; }
```

When the repo is itself a fork, fetch its parent's branches and tags into the clone too, so a fork that has pulled in the parent's later commits doesn't show them as its own:
```sh
d="forks-of/REPO.git" && git -C "$d" fetch -q --prune --no-tags --filter=tree:0 "https://github.com/PARENT-OWNER/PARENT-REPO.git" '+refs/heads/*:refs/upstream/heads/*' '+refs/tags/*:refs/upstream/tags/*'
```

Then, for each fork, fetch its branches beside the repo's and list the commits on them that no branch or tag of the repo (or of its parent) holds. Each command sets `d` again, since each may run in a shell of its own:
```sh
d="forks-of/REPO.git" &&
git -C "$d" fetch -q --prune --no-tags --filter=tree:0 "https://github.com/FORK-OWNER/FORK-REPO.git" '+refs/heads/*:refs/forks/FORK-OWNER/*' &&
git -C "$d" rev-list --count --glob='refs/forks/FORK-OWNER/*' --not --branches --tags --glob='refs/upstream/*' &&
git -C "$d" log --source --glob='refs/forks/FORK-OWNER/*' --not --branches --tags --glob='refs/upstream/*' --format='%S%x09%an%x09%ad%x09%s' --date=short | awk -F'\t' -v OFS='\t' -v branch=1 '{sub(/^refs\/forks\/[^\/]*\//, "", $branch); print}' | head -20
```
The first line is the count of the fork's commits that the repo doesn't hold; then up to 20 of them, newest first: a branch it's on, the author's name (never an email address), the date and the subject. When the count is over 20, say how many more there are. When it runs into the thousands, the fork most likely carries history from somewhere else, such as an old branch the user has since deleted: say so rather than list them. If the fetch fails (the fork was deleted, disabled or made private since the listing), say so for that fork and go on.

A fork of a fork shows its parent fork's commits as well as its own. Say which fork each commit first appears in when that's plain from the counts.

## Step 3: pick the ones worth a look

For each fork with commits, say in one line what they change, from the subjects (and, if the subjects say too little, the files a commit touches: `git -C "$d" show --stat --format= SHA`, which fetches that commit's trees on demand). Name the authors as git gives them, beside the fork owner's login.

Pick the forks worth a look: those whose commits add a feature or fix something the user's repo still lacks, those with stars or forks of their own (others build on them), and those pushed to in the last two years. Judge by what the commits do more than by stars. For each, write one line saying why, such as "fixes the two-digit year parsing the repo still gets wrong, 4 commits in 2025, 12 stars". A fork whose commits only bump versions, rename the project or add its owner's config is not worth a look. If none are, say so. If no fork could be read, no pick was made: say "Not available" with the reason, never that none are worth a look.

## Step 4: reply

1. **Worth a look**: one line per pick from Step 3, most relevant first, each starting with the fork's name in backticks.
2. **Forks with commits**: a table, most recently pushed first, with the fork, its owner's type, the commits (count, and the branches when not only the fork's default branch, from the listing), their authors, the latest commit's date, what they change, and its stars and forks. When no fork has commits of its own, leave the table out and say so in one line.
3. One line with the rest: how many forks nobody pushed to after making them, and how many were left out by the limit of 30.

Don't offer to contact anyone or open a pull request unless the user asks.
