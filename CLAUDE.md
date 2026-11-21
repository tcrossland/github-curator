# github-curator

A Claude plugin with three skills, `repo-review`, `stargazers` and `contributions`, that review a GitHub account's repos and recommend what to do with them. The [README](README.md) says what they do and how to install them.

## Where things are

- `skills/`: what ships. `repo-review/SKILL.md`, with the overview and triage steps in `overview.md` and `triage.md` beside it, the quote checker `verify_run.py` and `scorecard-template.html`, which renders all three modes; `stargazers/SKILL.md`; and `contributions/SKILL.md`.
- `docs/README.md`: notes for working on the plugin. The README at the root ships in the zip, so it links nothing outside it.
- `docs/design.md`: why the skills work the way they do. Read it before changing a rule.
- `docs/github-facts.md`: every behaviour of GitHub or Claude the skills rely on, with its source and the date it was checked.
- `docs/backlog.md`: what to build next, in order, each item with its "done when".
- `CHANGELOG.md`: what changed for a user of the plugin, one entry per release, with changes not yet released under Unreleased. It ships in the zip.

## Changing a skill

- `SKILL.md` loads in full on every run, so it holds instructions only. Put the reasons in `docs/design.md`. Steps used in only one mode go in that mode's file beside it.
- The skills only recommend. Never add a step that archives, deletes, pins, changes a repo's visibility, closes an issue or pull request, or contacts anyone.
- Before relying on a behaviour of GitHub or Claude, check `docs/github-facts.md`. A new fact goes there with its source ("Seen", or a link) and the date; anything not checked is marked **unverified**.
- A claude.ai chat's or run's own account of what happened is a claim: record a fact only from a command's output, a status code or the proxy's message, and mark the rest **unverified**.
- The skills run on claude.ai as well as in Claude Code, and a claude.ai session can't reach much of what works in a local shell: GraphQL, unscoped paths, unattached repos and cross-fork compare are all refused. The facts table's claude.ai section lists what works there. Don't assume a route that works here works there.
- Keep anything about a specific person or private repo out of shipped files.
- Try a change to a rule or the template with `no-publish`, so the live scorecard isn't republished.
- Test a new version in a session started after it synced. An open session and its subagents keep the skill text they loaded.

## Tests

```sh
python3 -m unittest discover tests
node --test tests/*.test.mjs
```

The Python tests run the code in the skills as it stands: the quote checker from `skills/repo-review/verify_run.py`, and the code blocks in each `SKILL.md`, found by their content: in `repo-review`, the timing script by `'reset'`, the logging line by `rate_limit`, the reply counts by `'flagged'`, the commit listing by `commits?per_page=100`, the issue listing by `issues?state=open`, the inline reply lookup by `/comments?per_page=100`, the Contributors script by `mine`, the secrets scan by `--redact` and its fetch on claude.ai by `checksums.txt`, a fork's commits by `refs/parent/` and a README's opening by `sparse-checkout`; in `triage.md`, the pull-request search by `-user:OWNER`; in `stargazers`, the repo listings by `users/LOGIN/repos` and `orgs/ORG/repos`, and the search that lists starred repos on claude.ai by `search/repositories?q=user:LOGIN`; in `contributions`, the listings by `is:public`, `is:private` and `per_page=1'`, the organisations by `user/memberships/orgs`, the repo search by `search/repositories` and the grouping script by `employers`. Keep those markers. A new snippet that calls `gh` needs a stand-in `gh` in its test that checks its arguments and runs the snippet's own `--jq`, as `tests/test_timings.py` does. A snippet that calls `git` runs against local repos served over `file://`, as `tests/test_git_routes.py` does.

The behaviour evals in `evals/` check the skills' calls on known cases, offline, with `scripts/evals.sh` (`claude plugin eval` underneath; it needs the CLI signed in, and costs real tokens). Each case names, in its graders, the rule it guards; a rule change that should change a case's call changes the case in the same commit. How much to run:

- A change to a rule: only the cases whose graders name it, once each, without the runs without the plugin (`--case NAME --runs 1 --ablation none`). A case tagged `repeat` keeps its own runs: leave out `--runs`. If no case guards the rule, say so in the commit.
- A rewrite or move of text in a `SKILL.md` that every case reads: every case, `--runs 1 --ablation none`.
- Before cutting a release: the full suite, `scripts/evals.sh` with no arguments.
- Nothing else needs them: the template, tests, scripts, docs, and fields copied as they are.

Runs go one at a time unless given `-j N` (up to 8), which `scripts/evals.sh` passes on: the full suite took 43 minutes one at a time, so run it with `-j 4`. The runs share one rate limit.

## Releasing

Add each user-facing change to `## Unreleased` in `CHANGELOG.md`, in the same commit as the change. Leave `version` alone until the user says to cut a release. Then, in one `chore(release): X.Y.Z` commit, rename Unreleased to the version and date and raise `version` in `.claude-plugin/plugin.json`, and build the zip with `scripts/package.sh`, which also validates the manifest. The user uploads it to claude.ai.

## Writing

British English, no em-dashes, plain words. Commit messages follow Conventional Commits: a `type(scope): subject` line in the imperative (types `feat`, `fix`, `docs`, `build`, `test`, `refactor`, `chore`; scopes such as `repo-review`, `stargazers`, `backlog` and `facts` for `docs/github-facts.md`), a blank line, then a wrapped body saying what changed and why.

## Working agreement

- Commit on a branch; the user reviews it, then `main` is fast-forwarded to it. Never push unless asked.
- Update the backlog in the same commit as the work it tracks. A done item is deleted, with its summary row: the changelog and the commit that closes it record it. Only when an open item depends on what it found does a short section under Done keep that part.
- Checks on claude.ai are prompts the user pastes into a claude.ai chat. Their findings go into `docs/github-facts.md` and the backlog. A prompt that attaches repos tells the chat not to clone them unless a step needs a clone, since `add_repo`'s result tells it to clone at once.
