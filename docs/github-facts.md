# Facts the skills rely on

The behaviours of GitHub and of Claude's plugin system that the skills state or depend on. Each fact has its source and the date it was checked. Platform behaviour changes, so recheck a fact before relying on it in a new rule, and update its date when you do.

"Seen" means it was seen in a real call rather than read in documentation.

## Repo actions

| Fact | Source | Checked |
|---|---|---|
| Changing visibility, in either direction, erases a repo's stars and watchers. | [Setting repository visibility](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility) | 2026-11-19 |
| Making a public repo private detaches its public forks, which stay public. | Same page | 2026-11-19 |
| Archiving makes issues, pull requests, comments, code, releases and more read-only. GitHub recommends closing issues and pull requests, and updating the README and description, first. Unarchiving is possible. | [Archiving repositories](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories) | 2026-11-19 |
| A deleted repo can be restored within 90 days, unless it was part of a fork network that isn't empty. | [Restoring a deleted repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/restoring-a-deleted-repository) | 2026-11-19 |
| Deleting a public repo doesn't delete its forks. Deleting a private repo deletes its forks. | [Deleting a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/deleting-a-repository) | 2026-11-19 |
| `gh repo delete OWNER/REPO` asks for confirmation unless given `--yes`, and needs the `delete_repo` scope (`gh auth refresh -s delete_repo`). | `gh repo delete --help`, gh 2.105.0 | 2026-11-19 |

## Profile pins

| Fact | Source | Checked |
|---|---|---|
| A profile shows up to six pinned repositories and gists, combined. | [Pinning items to your profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/pinning-items-to-your-profile) | 2026-11-19 |
| GraphQL lists pins (`user.pinnedItems`). No REST endpoint for them was found. | Seen with `gh api graphql` | 2026-11-19 |
| WebFetch of the profile page returns the pins, but names the owner only for repos owned by someone else. The owner of the rest is in each link's path. | Seen | 2026-11-19 |

## API behaviour

| Fact | Source | Checked |
|---|---|---|
| The issues endpoint also returns pull requests (entries with a `pull_request` field). Paginated counts of open issues plus open pull requests equal the repo's `open_issues_count` (cli/cli: 1081 + 60 = 1141). | Seen | 2026-11-19 |
| A fork's `ahead_by` from the compare endpoint can run into the thousands when its default branch has drifted from the parent's (seen: 9,897 ahead, an old `master` against the parent's `main`, none of the commits the fork owner's). | Seen | 2026-11-19 |
| The `author=` filter on the commits endpoint misses commits made under an email that isn't linked to the account; those commits have no `author.login` (seen: 6 of the fork owner's commits, none found by the filter). | Seen | 2026-11-19 |
| A repo's stargazers are listed only to its owner. For anyone else's public repo, `repos/OWNER/REPO/stargazers` returns 404 and GraphQL's `stargazers` returns no edges, while `stargazers_count` and `stargazerCount` still give the count (seen on `cli/cli`, `octocat/Hello-World` and `GAM-team/got-your-back`; the user's own repo listed normally). Whether push access is enough isn't tested, and the change hasn't been checked against GitHub's docs or changelog. | Seen | 2026-11-19 |
| Issue search results for pull requests include `pull_request.merged_at`. | Seen | 2026-11-19 |
| The repo listing (`user/repos`) includes `license`, with an `spdx_id`, or null when GitHub finds no licence file (seen: 10 of 23 of the user's own repos on the first page). GitHub reports a licence file it can't identify as `NOASSERTION`. | Seen, except `NOASSERTION`: not seen, and not yet checked against GitHub's docs (**unverified**) | 2026-11-19 |
| `repos/OWNER/REPO/community/profile` gives a `health_percentage` and which community files exist. | Seen | 2026-11-19 |
| Topic search (`topic:A+topic:B`) can rank only loosely related repos first; keyword search returns many results, also loosely ranked. | Seen | 2026-11-19 |
| Traffic covers the last 14 days and needs push access. | Stated in the skill before this file existed; not rechecked | — |

## Claude plugins and skills

| Fact | Source | Checked |
|---|---|---|
| The manifest goes at `.claude-plugin/plugin.json`; only `name` is required. Skills are found at `skills/<name>/SKILL.md`. | [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference.md) | 2026-11-19 |
| `claude plugin validate` warns when `version` or `author` is missing. | Seen | 2026-11-19 |
| A top-level `bin/` directory stops claude.ai and Cowork from installing a plugin. | Manifest reference | 2026-11-19 |
| Everyone who installs a plugin receives all its files. | [Build a plugin](https://claude.com/docs/plugins/build.md) | 2026-11-19 |
| Supporting files in a skill folder ship with the skill. `${CLAUDE_SKILL_DIR}` is filled in by Claude Code and Cowork; in chat on claude.ai, refer to a file by its path relative to `SKILL.md`. | [Skills how-to](https://claude.com/docs/skills/how-to.md), [Skills](https://code.claude.com/docs/en/skills) | 2026-11-19 |
| The docs disagree on the description limit: 200 characters in a help article, 1,024 in the skills how-to. A 263-character description uploaded and synced without error. | [Help article](https://support.claude.com/en/articles/12512198), how-to; seen | 2026-11-19 |
| Uploads are a zip, holding either the plugin's contents or a single top-level folder. | Build a plugin | 2026-11-19 |
